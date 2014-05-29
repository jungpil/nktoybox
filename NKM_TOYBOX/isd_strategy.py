'''
NK Modeling - Modularity + ISD Style
Jungpil Hahn and Taekyung Kim
2014
Information Systems @NUS

isd_strategy.py
'''

import numpy as np
from simulator import AdapterBehavior

class AdapterBehaviorAgileTeam(AdapterBehavior):
    """
|  Behavior of developers who adopts the agile methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        agent.expected_performance = self.agent_clan.landscape.get_noised_score_of_location_by_id(agent.my_id)
        current_score = agent.true_performance #casue agile gets feedback right away
        new_id = agent.my_id
        new_performance = agent.true_performance
        #mark current location
        agent.visited_ids[new_id] = 'v' #for sure TODO
        neighbors_np = np.array(list(neighbors),dtype=np.int)
        np.random.shuffle(neighbors_np)
        for neighbor_id in np.nditer(neighbors_np):
            new_score = self.agent_clan.landscape.get_noised_score_of_location_by_id(int(neighbor_id))
            if current_score < new_score and not agent.visited_ids.has_key(int(neighbor_id)):
                new_id = int(neighbor_id)
                # feedback from customers
                agent.expected_performance = new_score
                new_performance = self.agent_clan.landscape.get_score_of_location_by_id(int(neighbor_id))
                # visited
                agent.visited_ids[new_id]='v'
                break
        return (new_id,new_performance)
class AdapterBehaviorWaterfallTeam(AdapterBehavior):
    """
|  Behavior of developers who adopt the waterfall methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        """
|  Greed plan? Somewhat like...
        """
        neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        #agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        #agent.expected_performance = self.agent_clan.landscape.get_noised_score_of_location_by_id(agent.my_id)
        if (agent.ct % agent.feedback_tick) == 0:
            current_score = agent.true_performance #TODO
            agent.expected_performance  = agent.true_performance  #Feedback
        else:
            current_score = agent.expected_performance
        new_scores = map(self.agent_clan.landscape.get_noised_score_of_location_by_id,neighbors) #noised score
        np_scores = np.array(new_scores)
        new_id = agent.my_id
        new_performance = agent.true_performance
        #mark current location
        agent.visited_ids[new_id] = 'v' #for sure TODO
        if len(np_scores) > 0:
            max_v = np_scores.max()
            max_who = list(neighbors)[np.where(np_scores == max_v)[0]]
            if current_score < max_v and not agent.visited_ids.has_key(int(max_who)): #if different agent is better...
                new_id = max_who
                agent.expected_performance = max_v
                agent.true_performance = self.agent_clan.landscape.get_score_of_location_by_id(new_id)
                agent.visited_ids[max_who]='v'
                new_performance = agent.true_performance #return true score
        return (new_id,new_performance)
        