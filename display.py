import sdl2.ext
import sdl2
import numpy as np
import sdl2.sdlgfx
import pypangolin as pango
import cv2
from frame import Frame
from OpenGL.GL import *

class FeaturesPreview(object):
    def __init__(self, footage_path, queue) -> None:
        sdl2.ext.init()
        self.queue = queue
        self.cap = cv2.VideoCapture(footage_path)
        self.width, self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        self.fps = int(20)
        self.frame_manager = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_setFramerate(self.frame_manager, self.fps)
        sdl2.sdlgfx.SDL_initFramerate(self.frame_manager)

        self.window = sdl2.ext.Window("my_SLAM", size=(self.width, self.height))
        self.window.show()
        self.view()

    def draw(self, frame: np.ndarray) -> None:
        #quit event handler
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                exit(0)

        #actual drawing pixels
        pixels = sdl2.ext.pixels3d(self.window.get_surface())
        pixels[:, :, 0:3] = np.swapaxes(frame, 0, 1)
        self.window.refresh()

        #delaying frame for good fps
        sdl2.sdlgfx.SDL_framerateDelay(self.frame_manager)
    
    def view(self):
        #extracting frames from input, feature extraction, draw wrapper
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = Frame(np.array(frame))
                kps, des = frame.extract()
                export = list(map(lambda kp: (kp.pt[0], kp.pt[1]), kps))
                self.queue.put(export)
                self.draw(frame.process(kps))
            else:
                exit(0)

class Map3d(object):
    def __init__(self, queue):
        self.width = 1080
        self.height = 640
        self.window = pango.CreateWindowAndBind("my_SLAM_mapping", self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        self.scam = pango.OpenGlRenderState(
                    pango.ProjectionMatrix(self.width, self.height, 420, 420, self.width//2, self.height//2, 0.8, 100),
                    pango.ModelViewLookAt(0, -10, -8,
                                        0, 0, 0,
                                        0, -1, 0))
        handler = pango.Handler3D(self.scam)
        self.d_cam = pango.CreateDisplay()
        self.d_cam = self.d_cam.SetBounds(pango.Attach(0),pango.Attach(1),pango.Attach(0),pango.Attach(1), self.width/self.height)
        self.d_cam = self.d_cam.SetHandler(handler)
        self.queue = queue
        self.time = 0.0
        self.points = []
        self.run()

    def draw_points(self) -> None:
        color = np.random.random(3)
        self.points.append([color, self.queue.get(), self.time])
        for history in self.points:
            for point in history[1]:
                point_x, point_y, point_z = point[0] / 40, point[1] / 40, history[2]
                glColor3d(history[0][0], history[0][1], history[0][2])
                glVertex3d(point_x, point_y, point_z)
    
    def run(self):
        while not pango.ShouldQuit():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.d_cam.Activate(self.scam)
            glEnable(GL_POINT_SMOOTH)
            glPointSize(5)
            glBegin(GL_POINTS)
            self.draw_points()
            glEnd()
            pango.FinishFrame()
            self.time += 1
