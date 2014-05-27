from agent import Agent
class Student(Agent):
    def __init__(self, my_id, my_clan):
        Agent.__init__(self,my_id=my_id,my_clan=my_clan)
        self.plans = [[0,1,2,3,4,5]]