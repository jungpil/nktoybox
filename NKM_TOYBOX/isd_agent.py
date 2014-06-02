'''
isd_agent.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
from agent import Agent, AgentClan
from collections import deque
import random
import copy

class AgileDeveloper(Agent):
    """
|  A development team adopting the agile methodology
    """
    def __init__(self, my_id, my_clan):
        Agent.__init__(self,my_id=my_id,my_clan=my_clan)
        self.true_performance = 0
        self.expected_performance = 0
        self.wanna_be_my_id = -1
        self.plans = [[]]
class WaterfallDeveloper(Agent):
    """
|  A development team adopting the waterfall methodology
    """
    def __init__(self, my_id, my_clan):
        Agent.__init__(self,my_id=my_id,my_clan=my_clan)
        self.true_performance = 0
        self.expected_performance = 0
        self.wanna_be_my_id = -1
        self.plans = [[]]
        self.feedback_tick = 5 # timespan of taking feedback from users (or customers)
class AgileDeveloperClan(AgentClan):
    """
|  A clan is an abstract container that defines common attributes of agents
|  This class is about the clan of agile development teams
    """
    def __init__(self,landscape, processing_power, agent_class, population=1):
        AgentClan.__init__(self,landscape=landscape, processing_power=processing_power, agent_class=agent_class, population=population)
    def hatch_members(self):
        """
|  A clan is just a container. We need agents first. Make them.
        """
        assert self.iteration_plan != None, "No plans..."
        space_length = 1<<self.landscape.get_influence_matrix_N() #playground
        upper_limit = space_length-1 #set upper so that starts with zero
        self.tribe = deque() #tribe as deque collections (C type)
        add_member = self.tribe.append #declar append reference
        for _ in xrange(self.total_num): #for each...
            member_loc_id = random.randint(0,upper_limit)
            # locate agents randomly.
            agent = self.agent_class(member_loc_id,self)
            # create an agent
            agent.visited_ids[member_loc_id] = 'v' #visit
            # set up visited (of course, it can be duplicated at the stage of defining the initial status)
            agent.plans = copy.deepcopy(self.iteration_plan)
            # inherits plans...
            add_member(agent)
            # assign the agent as a clan member
        self.number_of_not_finished = self.total_num #for later use
class WaterfallDeveloperClan(AgentClan):
    """
|  A clan is an abstract container that defines common attributes of agents
|  This class is about the clan of waterfall development teams
    """
    def __init__(self,landscape, processing_power, agent_class, population=1, feedback_tick = 5):
        AgentClan.__init__(self,landscape=landscape, processing_power=processing_power, agent_class=agent_class, population=population)
        self.feedback_tick = feedback_tick # get feedback on every fifth tick
    def hatch_members(self):
        """
|  see AgileDeveloperClan...
        """
        assert self.iteration_plan != None, "No plans..."
        space_length = 1<<self.landscape.get_influence_matrix_N()
        upper_limit = space_length-1
        self.tribe = deque()
        add_member = self.tribe.append
        for _ in xrange(self.total_num):
            member_loc_id = random.randint(0,upper_limit)
            agent = self.agent_class(member_loc_id,self)
            agent.visited_ids[member_loc_id] = 'v' #visit
            agent.plans = copy.deepcopy(self.iteration_plan) # add
            agent.feedback_tick = self.feedback_tick
            add_member(agent)
        self.number_of_not_finished = self.total_num
    def __str__(self):
        rv = "Plan: %s\nProcessing Power: %d\nN: %d\nK: %d\nFeedback Tick: %d\n" % (self.iteration_plan,
                                                                                            self.myProcessingPower,
                                                                                            self.landscape.get_influence_matrix_N(),
                                                                                            self.landscape.get_influence_matrix_K(),
                                                                                            self.feedback_tick,)
        return rv
# END OF PROGRAM #