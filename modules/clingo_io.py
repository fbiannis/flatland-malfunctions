import pickle

from flatland.envs.rail_env import RailEnv

def load_environment_files(env_name: str) -> tuple:
    """Load both ASP and pickle environment files."""
    with open(f".\\envs\\lp\\{env_name}.lp", "r") as file:
        asp_environment = file.read()
    
    with open(f".\\envs\\pkl\\{env_name}.pkl", "rb") as file:
        rail_environment = pickle.load(file)
    
    return asp_environment, rail_environment

def load_encoding_files(primary_encoding_files, secondary_encoding_files) -> tuple:
    """Loads ASP encoding files and returns their contents as lists of strings."""
    def load_files(file_list):
        contents = []
        for file in file_list:
            with open(file, "r") as f:
                contents.append(f.read())
        return contents
    return load_files(primary_encoding_files), load_files(secondary_encoding_files)