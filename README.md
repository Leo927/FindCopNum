# FindCopNum
This is a program used to find the minimum cop number in the one visibility cop game. 
It is an implmentation of the algorithm described in cs412 project in fall 2020.

Environment:
	python 3.7.7,
	graphviz,
	pygraphviz,
	networkx,
	matplotlib

Source codes:
	constants.py: 
		used to store constants.

	label.py: 
		implemented a Label class.
		takes care of label manipulation. 
		have properties such as value to make the code more readable.
		

	rootedtree.py: 
		implemented a rootedtree class, 
		It takes care of rootedtree operation such as subtree, subForest, etc. 
		It also take care of tree saving, loading, generation. 


	copmanager.py:
		It implements the algorithm described in the project documentation

	test.py:
		unit testing module
	
	treedrawer.py:
		Used to draw labeled tree (non-labeled is also fine)
	

Author:
	Songhao Li

License:
	GNU General Public License