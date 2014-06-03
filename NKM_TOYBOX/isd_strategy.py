'''
isd_strategy.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''

import numpy as np
from simulator import AdapterBehavior
from isd_algorithm import linear_uncertainty

class AdapterBehaviorAgileTeam(AdapterBehavior):
    """
|  Behavior of developers who adopts the agile methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        if (agent.ct % 2) == 1: # last process (feedback)
            if agent.wanna_be_my_id >= 0:
                agent.my_id = agent.wanna_be_my_id
            agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
            agent.expected_performance = agent.true_performance
        else:
            # explore alternative (collect requirement information)
            current_score = agent.expected_performance #casue agile gets feedback right away
            neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
            neighbors_np = np.array(list(neighbors),dtype=np.int)
            np.random.shuffle(neighbors_np) #randomly select configuration (by luck)
            for neighbor_id in np.nditer(neighbors_np):
                new_score = self.agent_clan.landscape.get_noised_score_of_location_by_id(
                                    int(neighbor_id), 
                                    uncertainty_base = self.agent_clan.uncertainty_base,
                                    func = linear_uncertainty, 
                                    tick = agent.ct,
                                    total_tick = agent.tick_end)
                if current_score < new_score and not agent.visited_ids.has_key(int(neighbor_id)):
                    new_id = int(neighbor_id)
                    # feedback from customers
                    agent.expected_performance = new_score
                    agent.wanna_be_my_id = new_id
                    # visited
                    agent.visited_ids[new_id]='v'
                    break        
        new_id = agent.my_id
        new_performance = agent.true_performance
        return (new_id,new_performance)
    def my_profile(cls):
        rv = "----------------------------\n%s\n----------------------------\n" % ("Agile Development Team")
        return rv
    profile = classmethod(my_profile)
class AdapterBehaviorWaterfallTeam(AdapterBehavior):
    """
|  Behavior of developers who adopt the waterfall methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        if (agent.ct % agent.feedback_tick) == (agent.feedback_tick - 1): # last process
            agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
            agent.expected_performance = agent.true_performance
        elif (agent.ct % agent.feedback_tick) == 0:
            # requirement collection
            current_score = agent.expected_performance # the agent exactly know the evaluation from the market at the requirement stage
            neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
            new_scores = []
            new_scores_append = new_scores.append
            for neighbor_id in neighbors:
                lv = self.agent_clan.landscape.get_noised_score_of_location_by_id(
                                                                                                        int(neighbor_id), 
                                                                                                        func = linear_uncertainty,
                                                                                                        uncertainty_base = self.agent_clan.uncertainty_base,
                                                                                                        tick = agent.ct,
                                                                                                        total_tick = agent.tick_end) 
                new_scores_append(lv)
            np_scores = np.array(new_scores)
            if len(np_scores) > 0:
                max_v = np_scores.max()
                max_who = list(neighbors)[np.where(np_scores == max_v)[0]]
                if current_score < max_v and not agent.visited_ids.has_key(int(max_who)): #if different agent is better...
                    agent.wanna_be_my_id = max_who
        elif (agent.ct % agent.feedback_tick) == (agent.feedback_tick - 2): # n-1, deployment
            if agent.wanna_be_my_id >= 0:
                agent.my_id = agent.wanna_be_my_id
                agent.visited_ids[agent.my_id]='v'
        new_id = agent.my_id
        new_performance = agent.true_performance
        return (new_id,new_performance)
    def my_profile(cls):
        rv = "----------------------------\n%s\n----------------------------\n" % ("Waterfall Development Team")
        return rv
    profile = classmethod(my_profile)
# END OF PROGRAM #