'''
simulator.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
import numpy as np
import csv, time, gzip
import RandomGenerator

class SimRecord:
    def __init__(self, my_id, plan, ct, performance):
        self.location_id = my_id
        self.plan = self.str_plan(plan)
        self.ct = ct
        self.performance = performance
    def str_plan(self,plan_as_list):
        rv = "-".join(map(str,plan_as_list))
        return rv
class Simulator:
    def __init__(self,agent_clan):
        self.agent_clan = agent_clan
        self.simulation_record = []
    def run(self, tick_end, adapter_plan, adapter_behavior):
        agent_clan = self.agent_clan
        agent_clan.refresh_clan()
        self.adapter_plan_profile = adapter_plan.profile()
        self.adapter_behavior_profile = adapter_behavior.profile()
        for agent in agent_clan.tribe:
            my_plan = adapter_plan(self, adapter_behavior, agent_clan, agent, tick_end)
            my_plan.run()
    def write_record(self,agent):
        sr = SimRecord(agent.my_id,agent.plans,agent.ct,agent.performance)
        self.simulation_record.append(sr)
    def export_record(self,file_name):
        #standardized values
        land = self.agent_clan.landscape
        for sr in self.simulation_record:
            sr.performance = land.get_standardized_value(sr.performance)
        #for plot
        simple_simulation_record = [(sr.ct,sr.performance) for sr in self.simulation_record]
        nrow = len(simple_simulation_record)
        ncol = 2
        a = np.zeros(nrow*ncol,dtype='f').reshape(nrow,ncol)
        for k,l in enumerate(simple_simulation_record):
            a[k,0] = l[0]
            a[k,1] = l[1]
        file_name_plot = "%s_spreadsheet_plot.txt" % file_name
        np.savetxt(file_name_plot,a,fmt=['%d','%.4f'],delimiter=',')
        #for record
        file_name_record = "%s_record.gz" % file_name
        f_record = gzip.open(file_name_record,'wb')
        writer = csv.writer(f_record,lineterminator='\n',delimiter='\t')
        writer.writerow(['location_id','tick','plan','fitness'])
        for sr in self.simulation_record:
            writer.writerow([sr.location_id, sr.ct, sr.plan, sr.performance])
        f_record.close()
        #for profile
        plan_profile = self.adapter_plan_profile
        clan_profile =  self.agent_clan.__str__()
        behavior_profile = self.adapter_behavior_profile
        time_stamp = time.ctime()
        file_name_profile = "%s_profile.txt" % file_name
        f_profile = open(file_name_profile,'wb')
        f_profile.write("=========================================\n")
        f_profile.write("NK Landscape Simuation\n")
        f_profile.write("=========================================\n")
        f_profile.write("\nRandom seed:%d\n"%RandomGenerator.get_current_seed())
        f_profile.write("\n%s\n"%time_stamp)
        f_profile.write("\n%s\n"%plan_profile)
        f_profile.write("\n%s\n"%clan_profile)
        f_profile.write("\n%s\n"%behavior_profile)
        f_profile.close()
class AdapterPlan:
    def __init__(self, simulator, adapter_behavior, agent_clan, agent, tick_end):
        self.simulator = simulator
        self.adapter_behavior = adapter_behavior
        self.agent_clan = agent_clan
        self.agent = agent
        self.tick_end = tick_end
        self.fix_plan = self.agent_clan.fix_plan
        self.uncertainty_base = agent_clan.uncertainty_base
    def run(self):
        agent = self.agent
        current_behavior = self.adapter_behavior(self.agent_clan,agent)
        break_marker = False
        ct = 0
        agent.my_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        self.simulator.write_record(agent)
        while 1:
            for plan in agent.plans:
                agent.ct = ct
                (agent.my_id, agent.my_performance) = current_behavior.execute(agent, plan)
                ct += 1
                self.simulator.write_record(agent)
                if ct >= self.tick_end: # if ticks are over the target number,
                    break_marker = True
                    break
            if break_marker == True:
                break
    def my_profile(cls):
        pass
    profile = classmethod(my_profile)
class AdapterBehavior:
    def __init__(self, agent_clan, agent):
        self.agent_clan = agent_clan
    def execute(self, agent, plan):
        pass
    def my_profile(cls):
        pass
    profile = classmethod(my_profile)
# END OF PROGRAM #