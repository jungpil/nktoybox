'''
Created on 2014. 3. 20.
FOR TESTING!
@author: drtagkim
'''
#import agent
import numpy as np
'''
'''
class HillClimbingGreedAdaptive:
    def __init__(self,agent_clan):
        self.agent_clan = agent_clan
        self.simulation_record = []
    def run(self,plans,time_end,is_greed = True):
        '''
        Hill climbing
        if is_gree == True, it follows a greed algorithm;
        otherwise, it follows an adaptive searching behavior
        '''
        agent_clan = self.agent_clan #limit reference search scope
        agent_clan.refresh_clan() #refresh (new simulation starts)
        for agent in agent_clan.tribe:
            break_marker = False
            ct = 0 #current time
            agent.my_performance = agent_clan.landscape.get_score_of_location_by_id(agent.my_id) #for record
            self.write_record(agent.my_performance,ct)
            for plan in plans:
                ct += 1
                evaluation = True
                while 1:
                    if evaluation:
                        neighbors = set(agent_clan.landscape.who_are_neighbors(agent.my_id,plan,agent_clan.myProcessingPower,False)) #except me
                        current_score = agent.my_performance
                        new_scores = map(agent_clan.landscape.get_score_of_location_by_id,neighbors)
                        if is_greed == True:
                            np_scores = np.array(new_scores)
                            if len(np_scores) > 0:
                                max_v = np_scores.max()
                                max_who = list(neighbors)[np.where(np_scores == max_v)[0]]
                                if current_score <= max_v: #if different agent is better...
                                    agent.my_id = max_who
                                    agent.my_performance = max_v
                                else:
                                    evaluation = False # since the current position is optimal
                            else:
                                evaluation = False
                        else: # Adaptive
                            neighbors_np = np.array(list(neighbors),dtype=np.int)
                            np.random.shuffle(neighbors_np)
                            evaluation = False # assume that there is no leap
                            for neighbor_id in np.nditer(neighbors_np):
                                new_score = agent_clan.landscape.get_score_of_location_by_id(int(neighbor_id))
                                if current_score <= new_score:
                                    agent.my_id = int(neighbor_id)
                                    agent.my_performance = new_score
                                    evaluation = True # turns out you are wrong
                                    break # stop
                    #if
                    self.write_record(agent.my_performance,ct)
                    ct += 1 # draw a tick mark
                    if ct >= time_end: # if ticks are over the target number,
                        break_marker = True
                        break #stop the iteration and start a new run for another agent
                #while
                if break_marker == True:
                    break # since time is elapsed, there is no need to consider further plans.
    def write_record(self,performance,ct):
        self.simulation_record.append((ct,performance))
    def export_record(self,file_name):
        nrow = len(self.simulation_record)
        ncol = 2
        a = np.zeros(nrow*ncol,dtype='f').reshape(nrow,ncol)
        for k,l in enumerate(self.simulation_record):
            a[k,0] = l[0]
            a[k,1] = l[1]
        np.savetxt(file_name,a,fmt=['%d','%.4f'],delimiter=',')

