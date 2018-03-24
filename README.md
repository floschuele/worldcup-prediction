# worldcup-prediction
Soccer Worldcup Simulation Framework for Prediction


Easy to use
-------------
1. Set Parameters in "cup.py"
2. Start script using "python3 cup.py"
2. Simulation will be performed and results are printed in console

Parameters to set
------------------
1. Change parameter "self.model_id" to the model you want to test
2. Prameter "self.groups" is already filled with groups and teams of Worldcup 2018

Implemented Models
-------------------
1. Random results with up to 5 goals per team: self.model_id = "random"
2. Home always wins: self.model_id = "HomeAlwaysWins"

Ideas for further models
-----------------------
1. Deep learning for match prediction, train model with results of previous matches
2. Use bet odds, e.g. bwin, betfair
3. Use data from world ranking list
4. whatever...
