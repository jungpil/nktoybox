'''
cd D:\100_work\110_programming\113_liclipse_python\NKM
'''
from landscape import *
inf = construct_influence_matrix_from_file('inf/n16k4.txt','x')
lands = develop_landsacpes_from_influence_matrix(inf,100, 4)
save_landscapes(lands,'landscape_n16k4_100.nk')
'''
시작: 10:45
종료: 
'''