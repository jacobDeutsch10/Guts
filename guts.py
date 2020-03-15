import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from poker import Card, Rank, Hand
import random
import time
import datetime

hand_classes = ["_Trips", "_Pair", "_Pair_Kicker_", "_High"]

gen_classes = ["Trips", "Pair", "Pair w/ Kicker", "High"]


def is_trips(_hand):
    return _hand[0] == _hand[1] and _hand[0] == _hand[2]


def is_pair(_hand):
    return (_hand[0] == _hand[1] and _hand[1] != _hand[2]) or (_hand[0] != _hand[1] and _hand[1] == _hand[2])


def get_hand_class(_hand):
    if is_trips(_hand):
        return _hand[0] + hand_classes[0]
    elif is_pair(_hand):
        if _hand[0] == _hand[1]:
            return _hand[0] + hand_classes[2] + _hand[2]
        else:
            return _hand[2] + hand_classes[1]
    else:
        return _hand[2] + hand_classes[3]


def get_general_class(_hand):
    if is_trips(_hand):
        return gen_classes[0]
    elif is_pair(_hand):
        if _hand[0] == _hand[1]:
            return gen_classes[2]
        else:
            return gen_classes[1]
    else:
        return gen_classes[3]


deck = list(Card)
ranks = list(Rank)
combos = []
for i in ranks:
    for j in ranks:
        for k in ranks:
            combos.append(sorted([i, j, k]))
print(combos[0:20])
print(len(combos))
for key, i in enumerate(combos):
    for key2, j in enumerate(i):
        combos[key][key2] = str(j)
    combos[key] = ''.join(i)
current = time.time()

histo_dict = dict.fromkeys(combos, 0)
spec_class_dict = dict.fromkeys(combos,'')
gen_class_dict = dict.fromkeys(combos,'')
print(len(histo_dict.keys()))



runs = 100000

for i in range(runs):
    random.shuffle(deck)
    deal = deck[0:3]
    hand = sorted(deal)
    str_hand = [str(z.rank) for z in hand]
    str_hand = ''.join(str_hand)
    histo_dict[str_hand] += 1


num_trips = 0
for i in ranks:
    num = str(i)
    key = ''.join([num, num, num])
    print(key + " " + str(histo_dict[key]))
    num_trips += histo_dict[key]

# spec_class_dict: key=hand, val=specific class
# ex:{'222': '2_Trips', '223': '2_Pair_Kicker_3', '224': '2_Pair_Kicker_4',.....
spec_class_dict = dict.fromkeys(combos, '')

# gen_class_dict: key=hand, val=general class
# ex: {'222': 'Trips', '223': 'Pair w/ Kicker', '224': 'Pair w/ Kicker',...
gen_class_dict = dict.fromkeys(combos, '')

# gen_count_dict: key=general class, val=count of class from simulation
# ex: {'Trips': 233, 'Pair': 8455, 'Pair w/ Kicker': 8395, 'High': 82917}
gen_count_dict = dict.fromkeys(gen_classes, 0)

for key in histo_dict.keys():
    gen_class_dict[key] = get_general_class(key)
    spec_class_dict[key] = get_hand_class(key)
    gen_count_dict[gen_class_dict[key]] += histo_dict[key]

print(spec_class_dict)
print(gen_class_dict)
print(gen_count_dict)


print("total: ", str(num_trips))
print(histo_dict)
plt.bar(histo_dict.keys(), histo_dict.values())
plt.show()
print(num_trips/runs)
histo_items = histo_dict.items()
histo_list = list(histo_items)
df = pd.DataFrame(histo_list)
current_DT = datetime.datetime.now()
filename = "guts_histogram_" + str(runs) + "_" + str(current_DT.strftime("%m%d_%H_%M")) + ".csv"
df.to_csv(filename, mode="w", header=False, index=False)
print(time.time()-current)
