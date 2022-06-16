import sdl2.ext
import sdl2
import numpy as np
from frame import Frame

class FeaturesPreview(object):
    def __init__(self, width: int, hegiht: int) -> None:
        sdl2.ext.init()
        self.width, self.height = width, hegiht
        self.window = sdl2.ext.Window("my_SLAM", size=(width, hegiht))
        self.window.show()

    def draw(self, frame: np.ndarray) -> None:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                exit(0)
        pixels = sdl2.ext.pixels3d(self.window.get_surface())
        print("here", pixels.shape)
        pixels[:, :, 0:3] = np.swapaxes(frame, 0, 1)
        self.window.refresh()


