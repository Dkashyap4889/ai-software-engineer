class Node:
    def __init__(self, name, llm=None):
        self.name = name
        self.llm = llm

    def execute(self, state):
        return state