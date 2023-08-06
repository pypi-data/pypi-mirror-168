#mvcpy

Molecular clustering analysis, utilizing SpringSaLad Software.
By Aniruddha Chattaraj and Compiled by Abdulsalam Raja. 
Release 0.0.1 - 8/24/22

##Instructions

1. Installation:

'''
pip install MVC_Py
'''

2. Generate molecular clustering analysis

'''
python

from mvcpy.ClusterAnalysis import mvc
 
	file = " "
	#runs = [0,1,2,3,4]
	ca = mvc.ClusterAnalysis(file, t_total=None, runs=None, withMonomer=True)
	print(ca)
	ca.getMeanTrajectory()
	ca.getSteadyStateDistribution(SS_timePoints=[0.003,0.004,0.005])

'''