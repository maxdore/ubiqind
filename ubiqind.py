import argparse
import random

# Read the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("rounds", type=int, help="number of rounds")
parser.add_argument("agents", type=int, help="number of agents")
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
        # density page 15
        peers = list(range(0,i)) + list(range(i+1,args.agents))
        agents.append({
            'prob_new_better': random.random(),
            'peers': peers,
        })
    if args.v:
        print("Agents initialized: " + str(agents))

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
print(str(len(fails)/float(args.rounds)) + " / " + str(sum(fails) / float(len(fails))))
