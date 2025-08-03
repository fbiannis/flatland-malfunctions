import os
import imageio.v2 as imageio

from flatland.utils.rendertools import RenderTool
from flatland.envs.rail_env import RailEnv

class RenderSetup:
    """
    Basic setup needed for rendering the environment and storing renders.

    Attributes:
        renderer (RenderTool): The tool used for rendering the environment.
        images (list): A list to store rendered images.
    """
    def __init__(self, environment: RailEnv):
        self.renderer = RenderTool(environment, gl="PILSVG")
        self.renderer.reset()
        self.images = []

    def render_frame(self, timestep: int, current_environment=None):
        # TODO: Fix the last 2 frames of the sim missing
        if current_environment:
            self.renderer.env = current_environment
        
        filename = 'tmp/frames/flatland_frame_{:04d}.png'.format(timestep)
        self.renderer.render_env(show=True, show_observations=False, show_predictions=False)
        self.renderer.gl.save_image(filename)
        self.renderer.reset()
        self.images.append(imageio.imread(filename))

    def render_and_save_gif(self, timestamp: float):
        os.makedirs(f"output/{timestamp}", exist_ok=True)
        imageio.mimsave(f"output/{timestamp}/animation.gif", self.images, loop=0, duration=240)