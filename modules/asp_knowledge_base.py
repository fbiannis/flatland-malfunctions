import clingo
from modules.convert import model_to_string

class AspKnowledgeBase:
    """
    A class for managing standard ASP knowledge.
        asp_environment (str): The ASP fact representation of the environment.
        asp_actions (list): A list storing ASP actions derived from the environment. Members are of type (str)
    Methods:
        __init__(asp_environment: str): Initializes the knowledge base with the given ASP environment.
        _build_asp_actions(asp_environment) -> str: Builds and returns ASP actions from the provided environment.
    """

    def __init__(self, asp_environment: str, primary_encodings: str):
        self.asp_environment = asp_environment
        self.primary_encodings = primary_encodings
        self.asp_solutions = []
        self.add_solution(self._build_asp_actions(asp_environment)) 
        # TODO: Maybe split out _build_asp_solution into a seperate function call, instead of within constructor?

    def _build_asp_actions(self, asp_environment: str) -> str:
        ctl = clingo.Control()
        ctl.add("base", [], self.asp_environment)
        for encoding in self.primary_encodings:
            ctl.add("base", [], encoding)
        ctl.ground([("base", [])])
        models = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                models.append(model_to_string(model))
        # Return just the first model. Is this good?
        return models[0]
    
    def build_new_solution(self, malfunctions: dict, method, timestep: int) -> str:
        return method(self, malfunctions, timestep)


    def add_solution(self, solution: str):
        """Adds the provided ASP solution string to the list of solutions"""
        self.asp_solutions.append(solution)
