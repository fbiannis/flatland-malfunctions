import clingo

from modules.asp_knowledge_base import AspKnowledgeBase

def resolve_by_added_waits(asp_knowledge_base: AspKnowledgeBase, malfunctions: dict, current_timestep: int) -> str:
    # TODO: See if ActionAgent cannot be used
    actions = []
    ctl = clingo.Control()
    ctl.add("base", [], asp_knowledge_base.asp_solutions[-1])
    ctl.ground([("base", [])])
    
    # Extract actions from the model
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            for symbol in model.symbols(shown=True):
                if symbol.name == "action":
                    args = symbol.arguments
                    train_id = args[0].arguments[0].number
                    action_type = str(args[1])
                    timestep = args[2].number 
                    
                    actions.append((train_id, action_type, timestep))
    
    actions.sort(key=lambda x: x[2])
    
    time_shifts = {}
    for agent_id, malfunction_duration in malfunctions.items():
        time_shifts[agent_id] = malfunction_duration
    
    new_actions = []

    for agent_id, malfunction_duration in malfunctions.items():
        for i in range(malfunction_duration):
            new_actions.append((agent_id, "wait", current_timestep + i))
    
    for train_id, action_type, timestep in actions:
        if train_id in time_shifts and timestep >= current_timestep:
            new_timestep = timestep + time_shifts[train_id]
            new_actions.append((train_id, action_type, new_timestep))
        else:
            new_actions.append((train_id, action_type, timestep))
    
    new_actions.sort(key=lambda x: x[2])
    
    result_lines = []
    for train_id, action_type, timestep in new_actions:
        result_lines.append(f"action(train({train_id}),{action_type},{timestep}).")
    
    return '\n'.join(result_lines) + '\n'

def resolve_by_primary_encoding(asp_knowledge_base: AspKnowledgeBase, malfunctions: dict, current_timestep: int) -> str:
    # TODO: Implement
    pass