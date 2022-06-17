import sdl2.ext
import sdl2
import numpy as np
import sdl2.sdlgfx

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
