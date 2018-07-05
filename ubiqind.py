import argparse
import random

# Read the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("network", help="type of network (circle, complete, wheel or density as a float)")
parser.add_argument("agents", type=int, help="number of agents")
parser.add_argument("rounds", type=int, help="number of rounds")
parser.add_argument("-v", help="Show debugging information", action='store_true')
args = parser.parse_args()


cur_round = 1

# The main loop
sucs = []
fails = []
while cur_round <= args.rounds:
    if args.v:
        print("Playing round " + str(cur_round))
    
    # Initializing all agents and parameters
    agents = []
    for i in range(args.agents):
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

        agents.append({
            'prob_new_better': random.random(),
            'peers': peers,
        })
    if args.v:
        print("Agents initialized:")
        for i in range(args.agents):
            print(str(i) + ": " + str(agents[i]))

    num_gens = 1
    while True:
        for a in agents:
            a['prob_new_better'] = a['prob_new_better'] + random.random()/10
            # pursue method, depending which they find better
            # update belief according to result of resp. experiment 
            # receive payoff

        # agents meet and discuss results
     
        if all(a['prob_new_better'] < .5 for a in agents):
            if args.v:
                print("All agents believe inferior method is better after generation " + str(num_gens))
            fails.append(num_gens)
            break

        if all(a['prob_new_better'] > .9999 for a in agents):
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


