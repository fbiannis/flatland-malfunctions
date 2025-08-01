import time
from argparse import ArgumentParser, Namespace

from asp.active_solver_encodings import primary_encoding_files, secondary_encoding_files
from modules.clingo_io import load_encoding_files, load_environment_files
from modules.asp_knowledge_base import AspKnowledgeBase
from modules.render_setup import RenderSetup
from modules.flatland_simulation import FlatlandSimulation


def get_arguments() -> Namespace:
    """Reads the command line arguments and returns them as a Namespace object"""
    parser = ArgumentParser(description="Solves a provided pickle flatland environment using ASP, simulates and outputs a gif of the solution")
    parser.add_argument("env", type=str, help="The name of the environment found in /envs/pkl/ or /envs/pl/. No file ending")
    parser.add_argument("--render", "-r", type=bool, default=True, help="Choose if a gif of the solution should be output. (Defaul: True)")
    return parser.parse_args()


def main():
    arguments: Namespace = get_arguments()
    asp_environment, environment = load_environment_files(arguments.env)
    primary_encodings, secondary_encodings = load_encoding_files(primary_encoding_files, secondary_encoding_files)
    render_setup = RenderSetup(environment) if arguments.render else None
    
    asp_knowledge = AspKnowledgeBase(asp_environment, primary_encodings)
    simulation = FlatlandSimulation(environment, asp_knowledge)

    while simulation.execute_timestep():
        if render_setup:
            render_setup.render_frame(simulation.timestep, simulation.environment)
    
    timestamp = time.time()
    if render_setup:
        render_setup.render_and_save_gif(timestamp)


if __name__ == "__main__":
    main()
