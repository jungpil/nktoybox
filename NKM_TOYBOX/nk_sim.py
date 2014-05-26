from landscape import construct_influence_matrix_from_file
from landscape import develop_landsacpes_from_influence_matrix
from landscape import FitnessContributionTable
from landscape import Landscape
from strategy import HillClimbing
from agent import AgentClan, Agent
import numpy as np
import sys
#----------------------------------------------------------
def create_land(fname):
    '''
    Let's create influence matrix.
    Parameters: filename, marker
    '''
    inf = construct_influence_matrix_from_file(fname,'x')
    '''
    Create landscape
    Parameters: influence matrix, how many?, number of processors
    '''
    print "...Landscape..."
    lands = develop_landsacpes_from_influence_matrix(inf,1,processors = 1) #list object
    assert len(lands) > 0, "At least one land should be defined."
    land = lands[0]
    print "......complete"
    return land
def create_players(landscape,number_of_players):
    print "...Players..."
    processing_power = 1
    agent_clan = AgentClan(landscape,processing_power,Agent,number_of_players)
    agent_clan.name_called("Testers") #name it
    agent_clan.hatch_members() #hatch members
    print "......complete"
    return agent_clan
def execute_simulation(agent_clan,plan,time_end):
    print "...Simulation starts..."
    strategy = HillClimbing(agent_clan,1)
    for i in range(100):
        sys.stdout.write(".")
        strategy.run(1,plan,time_end)
    print "\n......complete"
    return strategy
def write_result(strategy,file_name):
    print "...Recording..."
    strategy.export_record(file_name)
    print "......completed"
if __name__ =="__main__":
    if len(sys.argv) != 6:
        print """ Parameters...
  input file name
  output file name
  target evolution step
  number of players
  N in your model

School of Computing
National University of Singapore
     Jungpil Hahn (PhD)
     Taekyung Kim (PhD)
2014 All right reserved
        """
        sys.exit(0)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    time_end = int(sys.argv[3])
    nplayers = int(sys.argv[4])
    N = int(sys.argv[5])
    '''
    Plan
    '''
    plan = range(N)
    land = create_land(input_file)
    agent_clan = create_players(land,nplayers)
    strategy = execute_simulation(agent_clan,plan,time_end)
    write_result(strategy,output_file)
    print "Thank you."