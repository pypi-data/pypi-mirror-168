import depthai as dai
import numpy as np
import cv2
import roboflowoak.postprocs as postprocs
import threading


class DepthAIPipeline:
    def __init__(self, nn_path, size, resolution, class_names, cam_stream, colors, confidence=0.5, overlap=0.5, sensor_mode="THE_1080_P", stretch=False, depth=False, device=None, legacy=False):
        self.nn_path = nn_path
        self.size = size
        self.class_names = class_names
        self.cam_stream = cam_stream
        self.colors = colors
        self.stretch = stretch
        self.resolution = resolution
        self.dev = device
        self.depth = depth
        self.overlap = overlap
        self.confidence = confidence
        self.frames = []

        self.pipeline = dai.Pipeline()
        if legacy:
            self.pipeline.setOpenVINOVersion(dai.OpenVINO.Version.VERSION_2021_1)

        self.cam_rgb = self.pipeline.create(dai.node.ColorCamera)
        self.cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        self.cam_rgb.setResolution(getattr(dai.ColorCameraProperties.SensorResolution, sensor_mode))
        self.cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        self.cam_rgb.setInterleaved(False)

        self.xout_raw = self.pipeline.create(dai.node.XLinkOut)
        self.xout_raw.setStreamName("raw")
        self.xout_raw.input.setBlocking(False)
        self.xout_raw.input.setQueueSize(1)

        self.controlIn = self.pipeline.create(dai.node.XLinkIn)
        self.controlIn.setStreamName('control')
        self.controlIn.out.link(self.cam_rgb.inputControl)

        self.detection_nn = self.pipeline.createNeuralNetwork()
        try:
            self.detection_nn.setBlobPath(self.nn_path)
        except:
            raise Exception("Failure loading model...")


        if cam_stream:
            self.xout_rgb = self.pipeline.createXLinkOut()
            self.xout_rgb.setStreamName("rgb")
            #self.cam_rgb.video.link(self.xout_rgb.input)

        self.xout_nn = self.pipeline.createXLinkOut()
        self.xout_nn.setStreamName("nn")
        self.detection_nn.out.link(self.xout_nn.input)


        self.manip = self.pipeline.createImageManip()

        self.manip.initialConfig.setCropRect((0,0,1,1))
        self.manip.initialConfig.setResize(self.size)

        self.manip_out = self.pipeline.createXLinkOut()
        self.manip_out.setStreamName("manip")
        self.manip.out.link(self.manip_out.input)

        if self.stretch:
            self.manip.initialConfig.setKeepAspectRatio(False)
        self.manip.inputImage.setBlocking(True)
        self.manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)

        self.manip.out.link(self.detection_nn.input)
        self.cam_rgb.video.link(self.manip.inputImage)
        if cam_stream:
            self.cam_rgb.video.link(self.xout_raw.input)
            self.manip.out.link(self.xout_rgb.input)

        if self.depth:
            self.left = self.pipeline.create(dai.node.MonoCamera)
            self.right = self.pipeline.create(dai.node.MonoCamera)
            self.stereo = self.pipeline.create(dai.node.StereoDepth)

            self.depthOut = self.pipeline.create(dai.node.XLinkOut)

            self.depthOut.setStreamName("depth")

            monoResolution = dai.MonoCameraProperties.SensorResolution.THE_400_P
            fps = 30

            self.left.setResolution(monoResolution)
            self.left.setBoardSocket(dai.CameraBoardSocket.LEFT)
            self.right.setResolution(monoResolution)
            self.right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

            self.stereo.initialConfig.setConfidenceThreshold(245)
            self.stereo.setLeftRightCheck(True)
            self.stereo.setDepthAlign(dai.CameraBoardSocket.RGB)

            self.left.out.link(self.stereo.left)
            self.right.out.link(self.stereo.right)
            self.stereo.disparity.link(self.depthOut.input)


        if self.dev is None:
            available_devices = list_devices()
            if len(available_devices) == 0:
                default_device = None
            else:
                self.dev = available_devices[0]

        found, device_info = dai.Device.getDeviceByMxId(self.dev)

        if not found:
            print("Device Not Found")\

        self.device = dai.Device(self.pipeline, device_info)

        self.q_det = self.device.getOutputQueue(name="nn", maxSize=4, blocking=False)

        if self.depth:
            self.q_depth = self.device.getOutputQueue(name="depth", maxSize=4, blocking=False)

        if cam_stream:
            self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            self.q_raw = self.device.getOutputQueue(name="raw", maxSize=4, blocking=False)

        self.q_manip = self.device.getOutputQueue(name="manip", maxSize=4, blocking=False)

        frame_thread = threading.Thread(target=collect_frame_thread, args=(self,))
        frame_thread.start()

    def disparity_to_depth(self, disparity):
        if disparity == 0:
            return np.NaN
        return 441.25 * 7.5 / disparity

    def detection_depth(self, detections, depth):
        res = []
        sx = len(depth)/self.size[0]
        sy = len(depth[0])/self.size[1]

        depth = np.nan_to_num(depth, copy=False, nan=0)

        depth_map = self.disparity_to_depth(depth)

        for det in detections:
            x = (det[2]+det[0])/2
            y = (det[3]+det[1])/2
            x = int(x*sx)
            y = int(y*sy)
            d = depth_map[det[0]:det[2], det[1]:det[3]]
            dist = np.amin(d)
            res.append([det[0], det[1], det[2], det[3], det[4], det[5], dist])

        return res

    def camera_control(self, control):
        q_control = self.device.getInputQueue(name="control")
        q_control.send(control)


    def print_seq_nums(self):
        nums = [frame.getSequenceNum() for frame in self.frames]
        print("Current Frames: ", nums)
    def find_frame(self, in_det):
        for i, frame in enumerate(self.frames):
            if frame.getSequenceNum() == in_det.getSequenceNum():
                self.frames = self.frames[i:]
                return frame



    def get(self):
        if self.depth:
            in_depth = self.q_depth.get()

        in_manip = self.q_manip.get()

        in_det = self.q_det.get()

        detections = self.post_processing(in_det)

        depth = None

        if self.depth:
            depth = in_depth.getFrame()
            detections = self.detection_depth(detections, depth)


        if self.cam_stream:
            frame, frame_raw = self.process_frame(detections, in_det)
            return detections, frame, frame_raw, depth

        return detections, depth

    def process_frame(self, detections, in_det):
        frame_raw = None
        frame = None
        in_raw = self.find_frame(in_det)
        if not in_raw:
            return np.array([]), np.array([])

        frame = in_raw.getCvFrame()
        x_offset = int((in_raw.getWidth()-in_raw.getHeight())/2)
        x_max = in_raw.getWidth()-x_offset

        #frame = frame.reshape(shape)
        #frame = frame.transpose(1, 2, 0)
        frame = frame.astype(np.uint8)
        frame = np.ascontiguousarray(frame)
        if not self.stretch:
            frame = frame[:,x_offset:x_max,:]
        frame_raw = np.array(frame)

        if frame is not None:
            for detection in self.scale_detections(detections, (in_raw.getWidth(), in_raw.getHeight())):
                class_color = self.colors[detection[4]].strip("#")
                class_color = tuple(int(class_color[i:i + 2], 16) for i in (0, 2, 4))
                cv2.rectangle(frame, (detection[0], detection[1]), (detection[2], detection[3]), class_color, 2)
                cv2.putText(frame, detection[4], (detection[0] + 10, detection[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                            class_color)
                cv2.putText(frame, str(int(detection[5] * 100)) + "%", (detection[0] + 10, detection[1] + 40),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.5, class_color)

        return frame, frame_raw

    def scale_detections(self, detections, frame_size):

        sx = frame_size[0]/self.size[0]
        sy = frame_size[1]/self.size[1]
        if not self.stretch:
            sx = sy
        res = []
        for det in detections:
            res.append([
                int(det[0]*sx), int(det[1]*sy), int(det[2]*sx), int(det[3]*sy), det[4], det[5]
            ])

        return res

    def post_processing(self, in_det):
        if in_det == None:
            return []

        in_nn_layer = in_det.getLayerFp16('output')
        num_anchor_boxes = len(np.array(in_nn_layer)) / (len(self.class_names) + 5)
        tensors = np.reshape(np.array(in_nn_layer), (1, int(num_anchor_boxes), len(self.class_names) + 5))

        batch_detections_np = postprocs.w_np_non_max_suppression(tensors, len(self.class_names), conf_thres=self.confidence, nms_thres=self.overlap)

        detections = []
        if len(batch_detections_np) == 0:
            detections = []
        else:
            detections = postprocs.process_detections(batch_detections_np[0], self.size, class_filter=self.class_names,
                                            class_names=self.class_names)

        return detections

def collect_frame_thread(self):
    while True:
        if self.cam_stream:
            in_rgb = self.q_rgb.get()
            in_raw = self.q_raw.get()
            self.frames.append(in_raw)
def list_devices():
    available_devices = []
    for device in dai.Device.getAllAvailableDevices():
        available_devices.append(device.getMxId())
    return available_devices


