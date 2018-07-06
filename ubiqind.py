import argparse
import random
import numpy
import math 


# Read the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("network", help="type of network (circle, complete, wheel or density as a float)")
parser.add_argument("agents", type=int, help="number of agents")
parser.add_argument("rounds", type=int, help="number of rounds")
parser.add_argument("-v", help="Show debugging information", action='store_true')
args = parser.parse_args()


# Model parameters not given as command line arguments
args.pulls = 1000
args.ops1 = .4 #.499
args.ops2 = .5
args.maxprior = 2 


class Agent:
    """
    The agent class with helpers for initializing 
    and updating an individual scientist
    """
    def __init__(self, id):
        self.id = id
        a1 = args.maxprior - random.uniform(0, args.maxprior)
        b1 = args.maxprior - random.uniform(0, args.maxprior)
        a2 = args.maxprior - random.uniform(0, args.maxprior)
        b2 = args.maxprior - random.uniform(0, args.maxprior)
        self.a = [a1,a2]
        self.b = [a1+b1, a2+b2]

        if args.network == "complete":
            peers = list(range(0,i)) + list(range(i+1,args.agents))
        elif args.network == "circle":
            peers = [(i-1) % args.agents, (i+1) % args.agents]
        elif args.network == "wheel":
            if i == 0: 
                peers = list(range(1, args.agents))
            else:
                peers = [0, ((i-2) % (args.agents-1)) + 1, (i % (args.agents-1)) + 1]
        else:
            peers = []
            for j in range(args.agents):
                if i != j and float(args.network) > random.random():
                    peers.append(j)
        self.peers = peers
        if args.v:
            print("Init" + str(self)) 


    def __str__(self):
        return "Agent " + str(self.id) + ": " + str(self.a) + ", " + str(self.b) + ", " + str(self.peers)  

    def get_posterior(self):
        return [x/y for x, y in zip(self.a, self.b)]

    def snd_better(self):
        return True
        # return probsnd > .5

    def snd_confident(self):
        return True
        # return probsnd > .9999


cur_round = 1
sucs = []
fails = []

# The main loop
while cur_round <= args.rounds:
    if args.v:
        print("Playing round " + str(cur_round))
    
    # Initializing all agents and parameters
    agents = []
    for i in range(args.agents):
        agents.append(Agent(i))

    num_gens = 1
    while True:
        for a in agents:
            ops = args.ops1 if not a.snd_better() else args.ops2
            sucpulls = round(numpy.random.normal(args.pulls*ops, math.sqrt(args.pulls*ops*(1-ops))))
            if args.v:
                print("Agent " + str(a.id) + " pulled: " + str(sucpulls))

            # For Testing:
            
            # a['prob_new_better'] = a['prob_new_better'] + random.random()/10
            # update belief according to result of resp. experiment 
            # receive payoff
            # cf Bala Goyal p. 10

        # agents meet and discuss results

        if all(not a.snd_better() for a in agents):
            if args.v:
                print("All agents believe inferior method is better after generation " + str(num_gens))
            fails.append(num_gens)
            break

        if all(a.snd_confident() for a in agents):
            if args.v:
                print("All agents are confident superior method is better after generation " + str(num_gens))
            sucs.append(num_gens)
            break

        num_gens = num_gens + 1

    cur_round = cur_round + 1

if args.v:
    print("Successful rounds:")
    print(sucs)
    print("Failed rounds:")
    print(fails)

print("Pct. Succ / Avg. Rounds")
print(str(len(sucs)/float(args.rounds)) + " / " + str(sum(sucs) / float(len(sucs))))

print("Pct. Failed / Avg. Rounds")
if len(fails) == 0:
    print("No failed rounds")
else:
    print(str(len(fails)/float(args.rounds)) + " / " + str(sum(fails) / float(len(fails))))


