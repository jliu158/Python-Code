Member of Group: Jiechen Liu	jliu100
		 Wentian Zhao	wzhao14
		 Boyuan  Tian   btian2

Part 1 Test:
python ExactInference.py

Then paste the instructions below to test different situations:
'aima-alarm.xml', 'B', {'J':True,'M':True}	# this is the example instruction for the alarm example, you can edit the ‘B’, ‘J’, ‘M’ for the alphabet stands for the any other variables: ‘B’, ‘E’, ‘A’, ‘J’, ‘M’

'aima-wet-grass.xml','R',{'S':True}		# this is the example instruction for the alarm example, you can edit the ‘R’, ‘S’ for the alphabet stands for the any other variables: ‘R’, ’S’, ‘C’, ‘W’

Part 2 Test:
1) Rejection sampling
python Rejection.py

100000, 'aima-alarm.xml', 'B', {'J':True,'M':True}	# this is the example instruction for the alarm example, you can edit the ‘B’, ‘J’, ‘M’ for the alphabet stands for the any other variables: ‘B’, ‘E’, ‘A’, ‘J’, ‘M’, also you can change the sampling number

1000, 'aima-wet-grass.xml', 'R', {'S':True}	# this is the example instruction for the alarm example, you can edit the ‘R’, ‘S’ for the alphabet stands for the any other variables: ‘R’, ’S’, ‘C’, ‘W’, also you can change the sampling number


2) Likelihood weighting
python Likelihood.py

10000, 'aima-alarm.xml', 'B', {'J':True,'M':True}	# this is the example instruction for the alarm example, you can edit the ‘B’, ‘J’, ‘M’ for the alphabet stands for the any other variables: ‘B’, ‘E’, ‘A’, ‘J’, ‘M’, also you can change the sampling number

1000, 'aima-wet-grass.xml', 'R', {'S':True}	# this is the example instruction for the alarm example, you can edit the ‘R’, ‘S’ for the alphabet stands for the any other variables: ‘R’, ’S’, ‘C’, ‘W’, also you can change the sampling number


3) Gibbs sampling
python GibbsAsk.py

1000, 'aima-alarm.xml', 'B', {'J':True,'M':True}	# this is the example instruction for the alarm example, you can edit the ‘B’, ‘J’, ‘M’ for the alphabet stands for the any other variables: ‘B’, ‘E’, ‘A’, ‘J’, ‘M’, also you can change the sampling number

1000, 'aima-wet-grass.xml', 'R', {'S':True}	# this is the example instruction for the alarm example, you can edit the ‘R’, ‘S’ for the alphabet stands for the any other variables: ‘R’, ’S’, ‘C’, ‘W’, also you can change the sampling number


TIPS: The original aims-alarm.xml has a typo in Definition of P(M|A), the column name of !A should be !M. I have attached the correct xml file in my folder, so please use it to test the program.

