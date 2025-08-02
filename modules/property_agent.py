import clingo
from modules.asp_knowledge_base import AspKnowledgeBase
from modules.environment_property_encodings import dependencies

class PropertyAgent:
    def __init__(self, asp_knowledge: list = None):
        self.ctl = clingo.Control()
        if asp_knowledge is None:
            return
        for item in asp_knowledge:
            self.ctl.add("base", [], item)
    
    def add(self, asp_knowledge: str):
        self.ctl.add("base", [], asp_knowledge)

    def add_list(self, asp_knowledge: list):
        for item in asp_knowledge:
            self.ctl.add("base", [], item)
        
    def add_asp_knowledge_base(self, asp_knowledge_base: AspKnowledgeBase):
        self.ctl.add("base", [], asp_knowledge_base.asp_environment)
        self.ctl.add("base", [], asp_knowledge_base.asp_solutions[-1])

    def ground(self):
        self.ctl.ground([("base",[])])

    def solve_for(self, properties: list):
        """
        Solves for the specified properties and returns the corresponding atoms.

        Args:
            properties (list of str): A list of property names to solve for.

        Returns:
            list: A list of atoms whose names match the specified properties.
        """
        if not isinstance(properties, list):
            properties = [properties]
        for property in properties:
            self._add_property_encoding(f"asp/environment_property/{property}.lp")
        atoms = self._solve()
        return [atom for atom in atoms if atom.name in properties]

    def _add_property_encoding(self, property_encoding: str):
        encodings_to_load = self._get_encoding_with_dependencies(property_encoding)
        for encoding in encodings_to_load:
            self.ctl.load(encoding)
    
    def _solve(self) -> list:
        with self.ctl.solve(yield_ = True) as handle:
            for model in handle:
                result = model.symbols(atoms = True)
                break  # Only take the first model...?
        return result

    def _get_encoding_with_dependencies(self, encoding: str) -> list:
        encodings = []
        stack = [encoding]
        visited = set()

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            encodings.append(current)
            visited.add(current)
            stack.extend(dependencies.get(current, []))

        return encodings
