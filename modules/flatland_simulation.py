from flatland.envs.rail_env import RailEnv

from modules.asp_knowledge_base import AspKnowledgeBase
from modules.malfunction_handling import get_problematic_by_delta, resolve_by_added_waits
from modules.convert import convert_asp_actions_to_list, convert_malfunctions_to_clingo

class FlatlandSimulation:
    def __init__(self, environment: RailEnv, asp_knowledge: AspKnowledgeBase):
        self.asp_knowledge = asp_knowledge
        self.environment = environment
        self.active_solution: list = convert_asp_actions_to_list(asp_knowledge.asp_solutions[0])
        self.timestep = 0
        self.malfunctions: dict = {}
        self.logs = []
    
    def execute_timestep(self) -> bool:
        """Execute one simulation timestep. Returns True if should continue."""
        self._deduct_malfunctions() # Should deduct be here?     
        self._log_agent_action()
        
        _, _, done, info = self.environment.step(self.active_solution[self.timestep])

        if done['__all__'] and self.timestep < len(self.active_solution) + 1:
            raise RuntimeError("Simulation finished early")
        
        self._handle_malfunction(info)

        self.timestep += 1
        # TODO: Fix the magic 2 here. Related to fixing missing render frames
        return self.timestep < len(self.active_solution) - 2 

    def _log_agent_action(self):
        action_map = {1:'move_left',2:'move_forward',3:'move_right',4:'wait'}
        state_map = {0:'waiting', 1:'ready to depart', 2:'malfunction (off map)', 3:'moving', 4:'stopped', 5:'malfunction (on map)', 6:'done'}
        direction_map = {0:'n', 1:'e', 2:'s', 3:'w'}

        for agent in self.active_solution[self.timestep]:
            action = self.active_solution[self.timestep][agent]
            action_value = action.value if hasattr(action, "value") else action
            self.logs.append(
                f"{agent};{self.timestep};{self.environment.agents[agent].position};"
                f"{direction_map[self.environment.agents[agent].direction]};"
                f"{state_map[self.environment.agents[agent].state]};"
                f"{action_map[action_value]}\n"
            )

    def _handle_malfunction(self, info: dict):
        new_malfunctions: dict = self._add_new_malfunctions(info)
        
        if not new_malfunctions:
            return
        asp_new_malfuntions: str = convert_malfunctions_to_clingo(new_malfunctions, self.timestep)
        if not self._check_malfunction_problematic(asp_new_malfuntions):
            new_solution = self.asp_knowledge.build_new_solution(new_malfunctions, resolve_by_added_waits, self.timestep)
        else:
            new_solution = self.asp_knowledge.build_new_solution(new_malfunctions, resolve_by_added_waits, self.timestep)
            
        self.asp_knowledge.add_solution(new_solution)
        self.active_solution = convert_asp_actions_to_list(new_solution)

    def _add_new_malfunctions(self, info: dict) -> dict:
        malfunctioning_info = info['malfunction']
        existing_malfunctions = self.malfunctions
        new_malfunctions = {train: duration for train, duration in malfunctioning_info.items() if duration > 0 and train not in existing_malfunctions}

        for train, duration in new_malfunctions.items():
            self.malfunctions.setdefault(train, duration)

        return new_malfunctions

    def _deduct_malfunctions(self):
        agents_to_remove = []
        for agent in list(self.malfunctions.keys()):
            self.malfunctions[agent] -= 1
            if self.malfunctions[agent] <= 0:
                agents_to_remove.append(agent)
        for agent in agents_to_remove:
            del self.malfunctions[agent]

    def _check_malfunction_problematic(self, asp_new_malfuntions: str) -> bool:
        return get_problematic_by_delta(self.asp_knowledge, asp_new_malfuntions)
