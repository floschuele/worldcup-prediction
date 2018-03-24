"""
03/2018
Florian Schüle <florianschuele@gmail.com>
World Cup simulator and predction of matches and winner
Framework for model testing


TODOS AND FIXMES:
- what happens in preliminary round when points and goals are equal?
- Draw must not appear in KO round - must be checked in model!

- Implement more Models
- Implement visual print of results

"""
import pprint
import time
import random


pprint = pprint.pprint
debug = False


class tournament:
    """
    Simulates a soccer tournement

    """

    def __init__(self):
        """
        Initialise tournament, define teams an necessary parameters

        """

        ########################################################################
        # Parameters to set                                                    
        ########################################################################
        
        # Define which model is used for simulation
        # Available: "random", "HomeAlwaysWins", 
        self.model_id = "random"

        # Define groups and teams
        self.groups = {"A": ["Russia", "Saudi Arabia", "Egypt", "Uruguay"],
                       "B": ["Portugal", "Spain", "Morocco", "Iran"],
                       "C": ["France", "Australia", "Peru", "Denmark"],
                       "D": ["Argentina", "Iceland", "Croatia", "Nigeria"],
                       "E": ["Brazil", "Switzerland", "Costa Rica", "Serbia"],
                       "F": ["Germany", "Mexico", "Sweden", "South Korea"],
                       "G": ["Belgium", "Panama", "Tunisia", "England"],
                       "H": ["Poland", "Senegal", "Colombia", "Japan"]}

        #########################################################################

        # Placeholders for results
        self.result_preliminary = {}  # create dict
        for group in self.groups:
            self.result_preliminary[group] = {}  # create subdict
            for team in self.groups[group]:
                self.result_preliminary[group][team] = {"Points": 0,
                                                        "Goals": 0}

        self.result_round_of_16 = {}
        for i in range(4):
            self.result_round_of_16[i] = ["winner_r16_0", "winner_r16_1"]
        self.result_quarter_finals = {}
        for i in range(2):
            self.result_quarter_finals[i] = ["winner_quarter_0", "winner_quarter_1"]
        self.result_semi_finals = {}
        for i in range(2):
            self.result_semi_finals[i] = ["winner_semi_0", "winner_semi_1"] # 2nd entry is losers which fight for 3rd place
        self.result_final = "champion"
        self.result_final_3rd = "3rd"

        # Match counter
        self.match_id = -1

        # List of matches and results
        self.matches = {}

    def match(self, HomeTeam, AwayTeam, stage):
        """
        Simulates single match between Home- and AwayTeam

        """
        # TODO
        # model defines match outcome

        model = self.model(self.model_id, HomeTeam, AwayTeam, stage)

        HomeGoals = model["HomeGoals"]
        AwayGoals = model["AwayGoals"]

        if HomeGoals > AwayGoals:
            result = "HomeWin"
        elif AwayGoals > HomeGoals:
            result = "AwayWin"
        elif HomeGoals == AwayGoals:
            result = "Draw"
            if HomeGoals == AwayGoals and stage != "preliminary": # Must not appear
                print("DRAW IS NOT POSSIBLE IN KNOCKOUT ROUND!!!")

        self.match_id += 1

        self.matches[self.match_id] = {"Match_id": self.match_id,
                                       "HomeTeam": HomeTeam,
                                       "AwayTeam": AwayTeam,
                                       "HomeGoals": HomeGoals,
                                       "AwayGoals": AwayGoals,
                                       "Result": result,
                                       "Stage": stage}
        return True

    def model(self, model_id, HomeTeam, AwayTeam, stage):
        """
        Predicts result of a match

        """
        
        # Random
        if model_id == "random":
            HomeGoals = random.randint(0,5)
            AwayGoals = random.randint(0,5)
            if stage != "preliminary": # Knockout round must not have Draws
                while HomeGoals == AwayGoals:
                    HomeGoals = random.randint(0,5)

        # Home always wins
        elif model_id == "HomeAlwaysWins":
            HomeGoals = 1
            AwayGoals = 0

        # Bet odds from bwin
        elif model_id == "bwin_odds":
            pass
        
        # Bet odds from Betfair
        elif model_id == "betfair_odds":
            pass

        # Using world ranking list
        elif model_id == "worldranking":
            pass

        # Deep learning from old matches
        elif model_id == "deep_learning":
            pass

        # Unknown model_id
        else:
            print("Model_id not known!!!")
            HomeGoals = 0
            AwayGoals = 0





        return {"HomeGoals": HomeGoals, "AwayGoals": AwayGoals}

    def knockout(self):
        """
        Perform knockout round simulation

        """
        self.round_of_16()
        if debug is True:
            print("\nResults round of 16:")
            pprint(worldcup.result_round_of_16)

        self.quarter_finals()
        if debug is True:
            print("\nResults quarter finals:")
            pprint(worldcup.result_quarter_finals)

        self.semi_finals()
        if debug is True:
            print("\nResults semi finals:")
            pprint(worldcup.result_semi_finals)

        self.final_3rd()
        if debug is True:
            print("\nResult final 3rd:")
            pprint(worldcup.result_final_3rd)

        self.final()
        if debug is True:
            print("\nResult final:")
            pprint(worldcup.result_final)

    def preliminary(self):
        """
        Simulates preliminary round:

        Each team plays one time against each other team

        """
        # 1. Perform matches and update points in results table

        # Loop throug all groups
        for group in self.groups:

            # Loop through matches 0-1, 0-2, 0-3
            for i in range(3):
                # Perform match and save data
                self.match(self.groups[group][0], self.groups[group][i+1], "preliminary")
                # update preliminary results
                if self.matches[self.match_id]["Result"] == "HomeWin":
                    self.result_preliminary[group][self.groups[group][0]]["Points"] += 3
                elif self.matches[self.match_id]["Result"] == "AwayWin":
                    self.result_preliminary[group][self.groups[group][i+1]]["Points"] += 3
                elif self.matches[self.match_id]["Result"] == "Draw":
                    self.result_preliminary[group][self.groups[group][0]]["Points"] += 1
                    self.result_preliminary[group][self.groups[group][i+1]]["Points"] += 1
                # Update Goal ratio
                self.result_preliminary[group][self.groups[group][0]]["Goals"] += self.matches[self.match_id]["HomeGoals"]
                self.result_preliminary[group][self.groups[group][0]]["Goals"] -= self.matches[self.match_id]["AwayGoals"]
                self.result_preliminary[group][self.groups[group][i+1]]["Goals"] -= self.matches[self.match_id]["HomeGoals"]
                self.result_preliminary[group][self.groups[group][i+1]]["Goals"] += self.matches[self.match_id]["AwayGoals"]

            # Loop through matches 1-2, 1-3
            for i in range(2):
                # Perform match and save data
                self.match(self.groups[group][1], self.groups[group][i+2], "preliminary")
                # update preliminary results
                if self.matches[self.match_id]["Result"] == "HomeWin":
                    self.result_preliminary[group][self.groups[group][1]]["Points"] += 3
                elif self.matches[self.match_id]["Result"] == "AwayWin":
                    self.result_preliminary[group][self.groups[group][i+2]]["Points"] += 3
                elif self.matches[self.match_id]["Result"] == "Draw":
                    self.result_preliminary[group][self.groups[group][1]]["Points"] += 1
                    self.result_preliminary[group][self.groups[group][i+2]]["Points"] += 1
                # Update Goal ratio
                self.result_preliminary[group][self.groups[group][1]]["Goals"] += self.matches[self.match_id]["HomeGoals"]
                self.result_preliminary[group][self.groups[group][1]]["Goals"] -= self.matches[self.match_id]["AwayGoals"]
                self.result_preliminary[group][self.groups[group][i+2]]["Goals"] -= self.matches[self.match_id]["HomeGoals"]
                self.result_preliminary[group][self.groups[group][i+2]]["Goals"] += self.matches[self.match_id]["AwayGoals"]

            # Perform match 2-3 and save data
            self.match(self.groups[group][2], self.groups[group][3], "preliminary")
            # update preliminary results
            if self.matches[self.match_id]["Result"] == "HomeWin":
                self.result_preliminary[group][self.groups[group][2]]["Points"] += 3
            elif self.matches[self.match_id]["Result"] == "AwayWin":
                self.result_preliminary[group][self.groups[group][3]]["Points"] += 3
            elif self.matches[self.match_id]["Result"] == "Draw":
                self.result_preliminary[group][self.groups[group][2]]["Points"] += 1
                self.result_preliminary[group][self.groups[group][3]]["Points"] += 1
            # Update Goal ratio
            self.result_preliminary[group][self.groups[group][2]]["Goals"] += self.matches[self.match_id]["HomeGoals"]
            self.result_preliminary[group][self.groups[group][2]]["Goals"] -= self.matches[self.match_id]["AwayGoals"]
            self.result_preliminary[group][self.groups[group][3]]["Goals"] -= self.matches[self.match_id]["HomeGoals"]
            self.result_preliminary[group][self.groups[group][3]]["Goals"] += self.matches[self.match_id]["AwayGoals"]

        # 2. Ranking

        # Loop through all groups
        for group in self.groups:
            
            # rank teams, but only first and second places are needed
            ranking_team = []
            ranking_points = []
            ranking_goals = []

            # fill lists
            for i in range(4):
               ranking_team.append(self.groups[group][i])
               ranking_points.append(self.result_preliminary[group][ranking_team[i]]["Points"])
               ranking_goals.append(self.result_preliminary[group][ranking_team[i]]["Goals"])

            # compare point[i=0,1,2] with the rest in list
            for i  in range(0, 3):
                for j in range(i+1, 4): # rest of the list
                    if ranking_points[i] < ranking_points[j]: # position i smaller j --> swap entries
                        ranking_team[i], ranking_team[j] = ranking_team[j], ranking_team[i] # swap list entries
                        ranking_points[i], ranking_points[j] = ranking_points[j], ranking_points[i]
                        ranking_goals[i], ranking_goals[j] = ranking_goals[j], ranking_goals[i]
                    elif (ranking_points[i] == ranking_points[j]) and (ranking_goals[i] < ranking_goals[j]): 
                        # points equal --> goal ratio
                        ranking_team[i], ranking_team[j] = ranking_team[j], ranking_team[i] # swap list entries
                        ranking_points[i], ranking_points[j] = ranking_points[j], ranking_points[i]
                        ranking_goals[i], ranking_goals[j] = ranking_goals[j], ranking_goals[i]

            self.result_preliminary[group]["Ranking"] = ranking_team

        if debug is True:
            print("\nResults of preliminary:")
            pprint(worldcup.result_preliminary)
        
        return True

    def round_of_16(self):
        """
        Simulates Round of 16:

        0:
            0: First A - Second B
            1: First C - Second D

        1:
            0: First E - Second F
            1: First G - Second H

        2:
            0: First B - Second A
            1: First D - Second C

        3:
            0: First F - Second E
            1: First H - Second G

        """

        # 0:0: Draw must not appear!
        self.match(self.result_preliminary["A"]["Ranking"][0], self.result_preliminary["B"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[0][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[0][0] = self.matches[self.match_id]["AwayTeam"]
        # 0:1:
        self.match(self.result_preliminary["C"]["Ranking"][0], self.result_preliminary["D"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[0][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[0][1] = self.matches[self.match_id]["AwayTeam"]
        
        # 1:0:
        self.match(self.result_preliminary["E"]["Ranking"][0], self.result_preliminary["F"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[1][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[1][0] = self.matches[self.match_id]["AwayTeam"]
        # 1:1:
        self.match(self.result_preliminary["G"]["Ranking"][0], self.result_preliminary["H"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[1][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[1][1] = self.matches[self.match_id]["AwayTeam"]

        # 2:0:
        self.match(self.result_preliminary["B"]["Ranking"][0], self.result_preliminary["A"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[2][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[2][0] = self.matches[self.match_id]["AwayTeam"]
        # 2:1:
        self.match(self.result_preliminary["D"]["Ranking"][0], self.result_preliminary["C"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[2][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[2][1] = self.matches[self.match_id]["AwayTeam"]

        # 3:0:
        self.match(self.result_preliminary["F"]["Ranking"][0], self.result_preliminary["E"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[3][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[3][0] = self.matches[self.match_id]["AwayTeam"]
        # 3:1:
        self.match(self.result_preliminary["H"]["Ranking"][0], self.result_preliminary["G"]["Ranking"][1], "round_of_16")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_round_of_16[3][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_round_of_16[3][1] = self.matches[self.match_id]["AwayTeam"]

        return True

    def quarter_finals(self):
        """
        Simulates Quarter Finals:

        0: Winners of round_of_16("0") 0:0: - 0:1:
        1: Winners of round_of_16("1") 1:0: - 1:1:
        2: Winners of round_of_16("2") 2:0: - 2:1:
        3: Winners of round_of_16("3") 3:0: - 3:1:

        """
        # 0 Draw must not appear!
        self.match(self.result_round_of_16[0][0], self.result_round_of_16[0][1], "quarter_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_quarter_finals[0][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_quarter_finals[0][0] = self.matches[self.match_id]["AwayTeam"]

        # 1
        self.match(self.result_round_of_16[1][0], self.result_round_of_16[1][1], "quarter_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_quarter_finals[0][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_quarter_finals[0][1] = self.matches[self.match_id]["AwayTeam"]

        # 2
        self.match(self.result_round_of_16[2][0], self.result_round_of_16[2][1], "quarter_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_quarter_finals[1][0] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_quarter_finals[1][0] = self.matches[self.match_id]["AwayTeam"]
        
        # 4
        self.match(self.result_round_of_16[3][0], self.result_round_of_16[3][1], "quarter_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_quarter_finals[1][1] = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_quarter_finals[1][1] = self.matches[self.match_id]["AwayTeam"]  

    def semi_finals(self):
        """
        Simulates Semi Finals:

        0: Winners of quarter_finals("0")
        1: Winners of quarter_finals("1")

        """
        # 0 Draw must not appear!
        self.match(self.result_quarter_finals[0][0], self.result_quarter_finals[0][1], "semi_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_semi_finals[0][0] = self.matches[self.match_id]["HomeTeam"]
            self.result_semi_finals[1][0] = self.matches[self.match_id]["AwayTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_semi_finals[0][0] = self.matches[self.match_id]["AwayTeam"]
            self.result_semi_finals[1][0] = self.matches[self.match_id]["HomeTeam"]

        # 1
        self.match(self.result_quarter_finals[1][0], self.result_quarter_finals[1][1], "semi_finals")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_semi_finals[0][1] = self.matches[self.match_id]["HomeTeam"]
            self.result_semi_finals[1][1] = self.matches[self.match_id]["AwayTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_semi_finals[0][1] = self.matches[self.match_id]["AwayTeam"]
            self.result_semi_finals[1][1] = self.matches[self.match_id]["HomeTeam"]

    def final(self):
        """
        Simulates final match:

        Winners of semi_finals()

        """
        self.match(self.result_semi_finals[0][0], self.result_semi_finals[0][1], "final")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_final = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_final = self.matches[self.match_id]["AwayTeam"]

    def final_3rd(self):
        """
        Simulates 3rd place match:

        Losers of semi_finals()

        """
        self.match(self.result_semi_finals[1][0], self.result_semi_finals[1][1], "final_3rd")
        if self.matches[self.match_id]["Result"] == "HomeWin":
            self.result_final_3rd = self.matches[self.match_id]["HomeTeam"]
        elif self.matches[self.match_id]["Result"] == "AwayWin":
            self.result_final_3rd = self.matches[self.match_id]["AwayTeam"]

    def print_preliminary_table(self):
        """
        Prints pretty table of preliminary round results

        """
        pass

    def print_knockout(self):
        """
        Prints Chart of matches of knockout round

        """
        pass

    def print_matches(self):
        """
        Print good looking match results

        """
        pass


if __name__ == "__main__":
    """
    Simulates the tournament using instance of tournament class

    """

    print("+++++++++++++++++++++++++++++++++++")
    print("+++++World Cup 2018 Simulation+++++")
    print("+++++++++++++++++++++++++++++++++++\n")
    print("Simulation started...\n")

    start = time.time()

    # Instance of tournament
    worldcup = tournament()

    # Preliminary Round
    print("Simulating preliminary round...")
    worldcup.preliminary()
    print("Done...\n")

    # Knockout
    print("Simulating knockout round...")
    worldcup.knockout()
    print("Done...\n")

    end = time.time()

    # PPrint all matches
    print("All Matches: ")
    #pprint(worldcup.matches)

    print("\nSimulation finished...\n")
    print("Finished in %s ms...\n" % str(round((end-start)*1000, 5)))

    if worldcup.result_final == "":
        print("WORLD CHAMPION 2018: Prediction FAILED")
    else:
        print("WORLD CHAMPION 2018: %s" % worldcup.result_final)
