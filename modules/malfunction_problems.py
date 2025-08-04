from modules.property_agent import PropertyAgent
from modules.asp_knowledge_base import AspKnowledgeBase

def get_problematic_by_delta(asp_knowledge_base: AspKnowledgeBase, malfunctions: str) -> bool:
    property_agent = PropertyAgent()
    property_agent.add_asp_knowledge_base(asp_knowledge_base)
    property_agent.add(malfunctions)

    atoms = property_agent.solve_for(["delta_conflict_point","delta_conflict_point_edge"])
    for atom in atoms:
        if atom.arguments[2] == atom.arguments[3]: 
            return True 
    return False