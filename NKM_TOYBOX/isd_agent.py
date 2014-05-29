'''
NK Modeling - Modularity + ISD Style
Jungpil Hahn and Taekyung Kim
2014
Information Systems @NUS

isd_agent.py
'''
from agent import Agent, AgentClan
from collections import deque
import random
import copy

class AgileDeveloper(Agent):
    def __init__(self, my_id, my_clan):
        Agent.__init__(self,my_id=my_id,my_clan=my_clan)
        self.true_performance = 0
        self.expected_performance = 0
        self.plans = [[]]
class WaterfallDeveloper(Agent):
    def __init__(self, my_id, my_clan):
        Agent.__init__(self,my_id=my_id,my_clan=my_clan)
        self.true_performance = 0
        self.expected_performance = 0
        self.plans = [[]]
        self.feedback_tick = 5
class AgileDeveloperClan(AgentClan):
    def __init__(self,landscape, processing_power, agent_class, population=1):
        AgentClan.__init__(self,landscape=landscape, processing_power=processing_power, agent_class=agent_class, population=population)
        self.plans = None
    def set_iteration_plan(self,iteration_plan):
        self.plans = copy.deepcopy(iteration_plan) #deep copy!
    def hatch_members(self):
        assert self.plans != None, "No plans..."
        space_length = 1<<self.landscape.get_influence_matrix_N()
        upper_limit = space_length-1
        self.tribe = deque()
        add_member = self.tribe.append
        for _ in xrange(self.total_num):
            member_loc_id = random.randint(0,upper_limit)
            agent = self.agent_class(member_loc_id,self)
            agent.visited_ids[member_loc_id] = 'v' #visit
            agent.plans = copy.deepcopy(self.plans) # add
            add_member(agent)
        self.number_of_not_finished = self.total_num
class WaterfallDeveloperClan(AgentClan):
    def __init__(self,landscape, processing_power, agent_class, population=1, feedback_tick = 5):
        AgentClan.__init__(self,landscape=landscape, processing_power=processing_power, agent_class=agent_class, population=population)
        self.plans = None
        self.feedback_tick = feedback_tick # get feedback on every fifth tick
    def set_iteration_plan(self,iteration_plan):
        self.plans = copy.deepcopy(iteration_plan) #deep copy!
    def hatch_members(self):
        assert self.plans != None, "No plans..."
        space_length = 1<<self.landscape.get_influence_matrix_N()
        upper_limit = space_length-1
        self.tribe = deque()
        add_member = self.tribe.append
        for _ in xrange(self.total_num):
            member_loc_id = random.randint(0,upper_limit)
            agent = self.agent_class(member_loc_id,self)
            agent.visited_ids[member_loc_id] = 'v' #visit
            agent.plans = copy.deepcopy(self.plans) # add
            agent.feedback_tick = self.feedback_tick
            add_member(agent)
        self.number_of_not_finished = self.total_num