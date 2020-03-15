import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from poker import Card, Rank
import random
import datetime
from functools import cmp_to_key


class GutsSimulator:

    def __init__(self, runs=10000):
        self.hand_classes = ["_Trips", "_Pair", "_Pair_Kicker_", "_High"]
        self.gen_classes = ["High",  "Pair", "Pair w/ Kicker", "Trips"]
        self.runs = runs
        self.deck = list(Card)
        ranks = list(Rank)
        self.combos = []
        for i in ranks:
            for j in ranks:
                for k in ranks:
                    self.combos.append(sorted([i, j, k]))

        for key, i in enumerate(self.combos):
            for key2, j in enumerate(i):
                self.combos[key][key2] = str(j)
            self.combos[key] = ''.join(i)

        self.histo_dict = dict.fromkeys(self.combos, 0)

        # spec_class_dict: key=hand, val=specific class
        # ex:{'222': '2_Trips', '223': '2_Pair_Kicker_3', '224': '2_Pair_Kicker_4',.....
        self.spec_class_dict = dict.fromkeys(self.combos, '')

        # gen_class_dict: key=hand, val=general class
        # ex: {'222': 'Trips', '223': 'Pair w/ Kicker', '224': 'Pair w/ Kicker',...
        self.gen_class_dict = dict.fromkeys(self.combos, '')

        # gen_count_dict: key=general class, val=count of class from simulation
        # ex: {'Trips': 233, 'Pair': 8455, 'Pair w/ Kicker': 8395, 'High': 82917}
        self.gen_count_dict = dict.fromkeys(self.gen_classes, 0)

    def is_trips(self, _hand):
        return _hand[0] == _hand[1] and _hand[0] == _hand[2]

    def is_pair(self, _hand):
        return (_hand[0] == _hand[1] and _hand[1] != _hand[2]) or (_hand[0] != _hand[1] and _hand[1] == _hand[2])

    def get_hand_class(self, _hand):
        if self.is_trips(_hand):
            return _hand[0] + self.hand_classes[0]
        elif self.is_pair(_hand):
            if _hand[0] == _hand[1]:
                return _hand[0] + self.hand_classes[2] + _hand[2]
            else:
                return _hand[2] + self.hand_classes[1]
        else:
            return _hand[2] + self.hand_classes[3]

    def get_general_class(self,  _hand):
        if self.is_trips(_hand):
            return self.gen_classes[3]
        elif self.is_pair(_hand):
            if _hand[0] == _hand[1]:
                return self.gen_classes[2]
            else:
                return self.gen_classes[1]
        else:
            return self.gen_classes[0]

    def simulate(self):
        for i in range(self.runs):
            random.shuffle(self.deck)
            deal = self.deck[0:3]
            hand = sorted(deal)
            str_hand = [str(z.rank) for z in hand]
            str_hand = ''.join(str_hand)
            self.histo_dict[str_hand] += 1
        self.populate_dicts()

    def populate_dicts(self):
        for key in self.histo_dict.keys():
            self.gen_class_dict[key] = self.get_general_class(key)
            self.spec_class_dict[key] = self.get_hand_class(key)
            self.gen_count_dict[self.gen_class_dict[key]] += self.histo_dict[key]

        print(self.spec_class_dict)
        print(self.gen_class_dict)
        print(self.gen_count_dict)

    def plot_histogram(self):
        print(self.histo_dict)
        plt.bar(self.histo_dict.keys(), self.histo_dict.values())
        plt.show()

    def sort_hand_strength(self):

        handlist = list(self.histo_dict.keys())
        # for i in range(0, len(handlist)):
        #   for j in range(i,len(handlist)):
            #  print(handlist[i] + " " + handlist[j] + " " + str(self.compare_hands(handlist[i], handlist[j])))
        print(sorted(handlist, key=cmp_to_key(self.compare_hands)))

    def compare_hands(self, h1, h2):
        print(h1)
        print(h2)
        gen1 = self.gen_class_dict[h1]
        gen2 = self.gen_class_dict[h2]
        spec1 = self.spec_class_dict[h1]
        spec2 = self.spec_class_dict[h2]
        ind1 = self.gen_classes.index(gen1)
        ind2 = self.gen_classes.index(gen2)
        rank1 = Rank(spec1[0])
        rank2 = Rank(spec2[0])
        trips = 3
        pwk = 2
        pair = 1
        high = 0

        if ind1 == trips or ind2 == trips:
            if ind1 != trips:
                return -1
            elif ind2 != trips:
                return 1
            else:
                return 1 if rank2 < rank1 else -1

        elif ind1 == high or ind2 == high:
            if ind1 != high:
                return 1
            elif ind2 != high:
                return -1
            elif rank1 == rank2:
                # if high cards are the same check first kicker
                k11 = Rank(h1[1])
                k21 = Rank(h2[1])
                if k11 != k21:
                    return 1 if k21 < k11 else -1
                else:
                    k12 = Rank(h1[0])
                    k22 = Rank(h2[0])
                    if k12 == k22:
                        return 0
                    else:
                        return 1 if k21 < k11 else -1
            else:
                return 1 if rank2 < rank1 else -1
        else:
            if rank1 > rank2:
                return 1
            elif rank1 < rank2:
                return -1
            else:
                if ind1 == pwk:
                    k1 = Rank(h1[2])
                else:
                    k1 = Rank(h1[0])
                if ind2 == pwk:
                    k2 = Rank(h2[2])
                else:
                    k2 = Rank(h2[0])
                if k1 == k2:
                    return 0
                else:
                    return 1 if k2 < k1 else -1

    def results_to_csv(self):
        histo_items = self.histo_dict.items()
        histo_list = list(histo_items)
        df = pd.DataFrame(histo_list)
        current_DT = datetime.datetime.now()
        filename = "guts_histogram_" + str(self.runs) + "_" + str(current_DT.strftime("%m%d_%H_%M")) + ".csv"
        df.to_csv(filename, mode="w", header=False, index=False)
