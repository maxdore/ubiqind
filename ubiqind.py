import argparse
import random
import numpy
import math
import copy


# Read the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("network", help="type of network (circle, complete, wheel or density as a float)")
parser.add_argument("agents", type=int, help="number of agents")
parser.add_argument("rounds", type=int, help="number of rounds")
parser.add_argument("-v", help="Show debugging information", action='store_true')
parser.add_argument("-s", help="Hide status information", action='store_true')
args = parser.parse_args()


# Model parameters not given as command line arguments
args.pulls = 10000
args.ops = [.499, .5] # .499, .499, .5] 
args.maxprior = 4
args.conflevel = .9999


class Agent:
    """
    The agent class with helpers for initializing
    and updating an individual scientist
    """
    def __init__(self, id):
        self.id = id
        self.a = []
        self.b = []
        for i in range(len(args.ops)):
            a = args.maxprior - random.uniform(0, args.maxprior)
            b = args.maxprior - random.uniform(0, args.maxprior)
            self.a.append(a)
            self.b.append(a+b)

        if args.network == "complete":
            self.peers = list(range(0,i)) + list(range(i+1,args.agents))
        elif args.network == "circle":
            self.peers = [(i-1) % args.agents, (i+1) % args.agents]
        elif args.network == "wheel":
            if i == 0:
                self.peers = list(range(1, args.agents))
            else:
                self.peers = [0, ((i-2) % (args.agents-1)) + 1, (i % (args.agents-1)) + 1]
        else:
            self.peers = []
            for j in range(args.agents):
                if i != j and float(args.network) > random.random():
                    self.peers.append(j)
        if args.v:
            print("Init" + str(self))

    def __str__(self):
        return "Agent " + str(self.id) + ": " + str(self.a) + ", " + str(self.b) + ", " + str(self.peers)

    def get_mean_beta(self):
        return [x/y for x, y in zip(self.a, self.b)]

    def belief(self):
        mean = self.get_mean_beta()
        return mean.index(max(mean))

    def confident(self):
        return self.get_confidence() > args.conflevel

    def get_confidence(self):
        mean = self.get_mean_beta()
        infBelief = min(mean)

        peers = [agents[p] for p in self.peers]
        if len(peers) > 0:
            signals = [args.ops[a.belief()] for a in peers]
            avgSignal = sum(signals) / float(len(signals))
        else:
            avgSignal = sum(args.ops) / float(len(args.ops))

        if avgSignal <= infBelief:
            return 0

        alpha = self.a[self.belief()]
        varepsilon = avgSignal - infBelief
        delta  = mean[self.belief()] - infBelief

        if args.v:
            print(str(infBelief) + " " + str(avgSignal) + " " + str(alpha) + " " + str(varepsilon) + " " + str(delta))

        if (2 * alpha - 1) * delta <= infBelief:
            return 0

        exitProb = 0.5 + 0.5 * self.erf (
          ((0 - 2 * alpha + 1) * delta + infBelief)
          / (math.sqrt((0 - 2 * alpha * delta + delta + infBelief)
          * (infBelief + varepsilon) * (0 - 1 + infBelief + varepsilon)
          / (varepsilon * (infBelief + delta)))
          * (infBelief + delta)))
        return 1 - exitProb

    def erf(self, x):
        t = (1 - .5 * x)
        return math.exp( 0 - x ** 2 - 1.26551223 + 1.00002368 / t
            + .37409196 / t ** 2 + 0.09678418 / t ** 3
            - .18628806 / t ** 4 + .27886807 / t ** 5
            - 1.13520398 / t ** 6 + 1.48851587 / t ** 7
            - .82215223 / t ** 8 + .17087277 / t ** 9) / t - 1


cur_round = 1
succs = []
fails = []

# The main loop
while cur_round <= args.rounds:
    if not args.s:
        print ("Round " + str(cur_round) , end="\r")

    # Initializing all agents and parameters
    agents = []
    for i in range(args.agents):
        agents.append(Agent(i))


    num_gens = 1
    while True:
        if args.v:
            print("Generation " + str(num_gens))

        # An agents pulls the bandit 
        for a in agents:
            ops = args.ops[a.belief()]
            a.succpulls = round(numpy.random.normal(args.pulls*ops, math.sqrt(args.pulls*ops*(1-ops))))

            if args.v:
                print("Agent " + str(a.id) + " pulled for theory " + str(int(a.belief())) + " : " + str(a.succpulls))

        # All agents share their successes
        newagents = copy.deepcopy(agents)
        for a in newagents: 
            gensuccs = [0 for o in args.ops]
            genpulls = [0 for o in args.ops]
            for peerid in a.peers + [a.id]:
                peer = agents[peerid]
                gensuccs[peer.belief()] = gensuccs[peer.belief()] + peer.succpulls
                genpulls[peer.belief()] = genpulls[peer.belief()] + args.pulls

            a.a = [x+y for x, y in zip(gensuccs, a.a)]
            a.b = [x+y for x, y in zip(genpulls, a.b)]

            if args.v:
                print("Updated " + str(a))

        agents = newagents

        if args.v:
            for a in agents:
                if a.get_confidence() < .5:
                    print("Agent " + str(a.id) + " believes in correct theory with: " + str(a.get_confidence()))

        if len(list(set((a.belief() for a in agents)))) == 1:
            if agents[0].belief() != len(args.ops) - 1:
                if args.v:
                    print("All agents believe in inferior method after generation " + str(num_gens))
                fails.append(num_gens)
                break
            elif all(a.confident() for a in agents):
                if args.v:
                    print("All agents are confident in superior method after generation " + str(num_gens))
                succs.append(num_gens)
                break

        num_gens = num_gens + 1
        if num_gens == 10000:
            if args.v:
                print("Round terminated")
                print(agents)
            break

    cur_round = cur_round + 1

if args.v:
    print("Successful rounds:")
    print(succs)
    print("Failed rounds:")
    print(fails)

pctsucc = str(len(succs)/float(args.rounds)) 
succgens = str(sum(succs) / float(len(succs))) if len(succs) > 0 else "/"
pctfail = str(len(fails)/float(args.rounds)) 
failgens = str(sum(fails) / float(len(fails))) if len(fails) > 0 else "/"

if args.v:
    print("Network / Scientists / Pct. Succ / Avg. gens to succ / Pct. Failed / Avg. gens to fail")

if not args.s:
    print("         ", end="\r")
    end = "\r"
else :
    end = "\n"
print(args.network + "\t" + str(args.agents) + "\t" + pctsucc + "\t" + succgens  + "\t" + pctfail + "\t" + failgens, end=end)
if not args.s:
    print("")
