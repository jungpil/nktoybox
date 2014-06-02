'''
agent.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
import numpy as np
from simulator import AdapterBehavior

class AdapterBehaviorGreed(AdapterBehavior):
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        current_score = agent.my_performance
        new_scores = map(self.agent_clan.landscape.get_score_of_location_by_id,neighbors)
        np_scores = np.array(new_scores)
        new_id = agent.my_id
        new_performance = agent.my_performance
        #mark current location
        agent.visited_ids[new_id] = 'v'
        if len(np_scores) > 0:
            max_v = np_scores.max()
            max_who = list(neighbors)[np.where(np_scores == max_v)[0]]
            if current_score < max_v and not agent.visited_ids.has_key(max_who): #if different agent is better...
                new_id = max_who
                new_performance = max_v
                agent.visited_ids[max_who]='v'
        return (new_id,new_performance)

class AdapterBehaviorAdaptive(AdapterBehavior):
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self,agent_clan,agent)
    def execute(self,agent,plan):
        neighbors = set(self.agent_clan.landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        current_score = agent.my_performance
        new_id = agent.my_id
        new_performance = agent.my_performance
        #mark current location
        agent.visited_ids[new_id] = 'v'
        neighbors_np = np.array(list(neighbors),dtype=np.int)
        np.random.shuffle(neighbors_np)
        for neighbor_id in np.nditer(neighbors_np):
            new_score = self.agent_clan.landscape.get_score_of_location_by_id(int(neighbor_id))
            if current_score < new_score and not agent.visited_ids.has_key(max_who):
                new_id = int(neighbor_id)
                new_performance = new_score
                agent.visited_ids[new_id]='v'
                break
        return (new_id,new_performance)
# END OF PROGRAM #