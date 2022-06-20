import sdl2.ext
import sdl2
import numpy as np
import sdl2.sdlgfx
import pypangolin as pango
from OpenGL.GL import *

class FeaturesPreview(object):
    def __init__(self, width: int, hegiht: int, fps: int) -> None:
        sdl2.ext.init()
        self.width, self.height = int(width), int(hegiht)

        self.fps = int(fps)
        self.frame_manager = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_setFramerate(self.frame_manager, self.fps)
        sdl2.sdlgfx.SDL_initFramerate(self.frame_manager)

        self.window = sdl2.ext.Window("my_SLAM", size=(self.width, self.height))
        self.window.show()

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
        self.run()

    def add_points(self, points):
        self.points = points

    def draw_points(self) -> None:
        color = np.random.random(3)
        for point in self.queue.get():
            point_x, point_y, point_z = point[0] / 75, point[1] / 75, 0
            glColor3d(color[0], color[1], color[2])
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
