#
#
#

import numpy as np

class Simulator:
    def __init__(self,agent_clan):
        self.agent_clan = agent_clan
        self.simulation_record = []
    def run(self, tick_end, adapter_plan, adapter_behavior):
        agent_clan = self.agent_clan
        agent_clan.refresh_clan()
        for agent in agent_clan.tribe:
            my_plan = adapter_plan(self, adapter_behavior, agent_clan, agent, tick_end)
            my_plan.run()
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
class AdapterPlan:
    def __init__(self, simulator, adapter_behavior, agent_clan, agent, tick_end):
        self.simulator = simulator
        self.adapter_behavior = adapter_behavior
        self.agent_clan = agent_clan
        self.agent = agent
        self.tick_end = tick_end
    def run(self):
        agent = self.agent
        current_behavior = self.adapter_behavior(self.agent_clan,agent)
        break_marker = False
        ct = 0
        agent.my_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        self.simulator.write_record(agent.my_performance,ct)
        while 1:
            for plan in agent.plans:
                (agent.my_id, agent.my_performance) = current_behavior.execute(agent, plan)
                ct += 1
                self.simulator.write_record(agent.my_performance,ct)
                if ct >= self.tick_end: # if ticks are over the target number,
                    break_marker = True
                    break
            if break_marker == True:
                break
class AdapterBehavior:
    def __init__(self, agent_clan, agent):
        self.agent_clan = agent_clan
    def execute(self, agent, plan):
        pass
        