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
        #rewrite from here
        agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        agent.expected_performance = agent.true_performance
        current_score = agent.expected_performance #casue agile gets feedback right away
        # base
        new_id = agent.my_id
        new_performance = agent.true_performance
        # search
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
                #new_id = int(neighbor_id)
                neighbor_id_int = int(neighbor_id)
                # marketing
                agent.expected_performance = new_score
                agent.wanna_be_my_id = new_id
                # feedback from customers
                new_score_true = self.agent_clan.landscape.get_score_of_location_by_id(neighbor_id_int)
                if agent.true_performance < new_score_true:
                    # success
                    new_id = neighbor_id_int
                    new_performance = new_score_true
                    # visited
                    agent.visited_ids[new_id]='v'
                    break
                else:
                    # fail
                    current_score = new_score_true
                    agent.my_id = neighbor_id_int
                    agent.visited_ids[agent.my_id] = 'v'
                    agent.true_performance = current_score
                    agent.expected_performance = current_score
                    new_id = agent.my_id
                    new_performance = current_score
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
        agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        agent.expected_performance = agent.true_performance
        # base
        new_id = agent.my_id
        new_performance = agent.true_performance
        # requirement collection
        current_score = agent.true_performance # exact information from the start
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
                new_id = max_who # jump to the location
                agent.visited_ids[new_id]='v'
                # feedback
                new_performance = self.agent_clan.landscape.get_score_of_location_by_id(new_id)
        return (new_id,new_performance)
    def my_profile(cls):
        rv = "----------------------------\n%s\n----------------------------\n" % ("Waterfall Development Team")
        return rv
    profile = classmethod(my_profile)
# END OF PROGRAM #