from clingo import Control, Model

from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_env import RailEnvActions
from flatland.utils.rendertools import RenderTool, AgentRenderVariant


def convert_to_clingo(env) -> str:
    """
    converts Flatland environment to clingo facts
    """
    # environment properties
    rail_map = env.rail.grid
    height, width, agents = env.height, env.width, env.agents
    clingo_str = f"% clingo representation of a Flatland environment\n% height: {height}, width: {width}, agents: {len(agents)}\n"
    clingo_str += f"\nglobal({env._max_episode_steps}).\n"

    # save start and end positions for each agent
    dir_map = {0:"n", 1:"e", 2:"s", 3:"w"}
    
    for agent_num, agent_info in enumerate(env.agents):
        init_y, init_x = agent_info.initial_position
        goal_y, goal_x = agent_info.target
        min_start, max_end = agent_info.earliest_departure, agent_info.latest_arrival
        speed = int(1/agent_info.speed_counter.speed) # inverse, e.g. 1/2 --> 2, 1/4 --> 4 etc.

        direction = dir_map[agent_info.initial_direction]
        clingo_str += f"\ntrain({agent_num}). "
        clingo_str += f"start({agent_num},({init_y},{init_x}),{min_start},{direction}). "
        clingo_str += f"end({agent_num},({goal_y},{goal_x}),{max_end}). "
        clingo_str += f"speed({agent_num},{speed}).\n"

    clingo_str += "\n"

    # create an atom for each cell in the environment
    #row_num = len(rail_map) - 1
    for row, row_array in enumerate(rail_map):
        for col, cval in enumerate(row_array):
            clingo_str += f"cell(({row},{col}), {cval}).\n"
        #row_num -= 1
        clingo_str+="\n"
        
    return(clingo_str)


def convert_malfunctions_to_clingo(malfunctions: dict, timestep: int) -> str:
    """ Returns the string of input malfunctions dict as asp fact
    
    Format: \"malfunction(train, duration, timestep)\""""
    facts = ""
    for train in malfunctions:
        duration = malfunctions[train]
        facts += f'malfunction({train},{duration},{timestep}).\n'
    return facts


def convert_asp_actions_to_list(asp_actions: str) -> list:
    """Converts a string of asp actions into a list, for use with flatland"""
    actions_list = []
    def action_model_to_list(model):
        # Extract actions from the model
        action_mapping = {
            "move_left": RailEnvActions.MOVE_LEFT,
            "move_forward": RailEnvActions.MOVE_FORWARD,
            "move_right": RailEnvActions.MOVE_RIGHT,
            "wait": RailEnvActions.STOP_MOVING,
            "do_nothing": RailEnvActions.DO_NOTHING
        }
        for atom in model.symbols(shown=True):
            if atom.name == "action":
                train_id = int(str(atom.arguments[0].arguments[0]))
                action_str = str(atom.arguments[1])
                timestep = int(str(atom.arguments[2]))
                # Ensure the actions_list is large enough
                while len(actions_list) <= timestep:
                    actions_list.append({})
                actions_list[timestep][train_id] = action_mapping.get(action_str, RailEnvActions.DO_NOTHING)

    ctl = Control()
    ctl.add("base", [], asp_actions)
    ctl.ground([("base", [])])
    ctl.solve(on_model=action_model_to_list)
    return actions_list

def model_to_string(model: Model) -> str:
    """
    Converts a clingo Model object to a string of atoms.
    """
    return "".join(f"{str(atom)}.\n" for atom in model.symbols(shown=True))