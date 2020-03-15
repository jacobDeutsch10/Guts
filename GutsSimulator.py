import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from poker import Card, Rank
import random
import datetime


class GutsSimulator:

    def __init__(self, runs=10000):
        self.hand_classes = ["_Trips", "_Pair", "_Pair_Kicker_", "_High"]
        self.gen_classes = ["Trips", "Pair", "Pair w/ Kicker", "High"]
        self.runs = runs
        self.deck = list(Card)
        ranks = list(Rank)
        combos = []
        for i in ranks:
            for j in ranks:
                for k in ranks:
                    combos.append(sorted([i, j, k]))

        for key, i in enumerate(combos):
            for key2, j in enumerate(i):
                combos[key][key2] = str(j)
            combos[key] = ''.join(i)

        self.histo_dict = dict.fromkeys(combos, 0)

        # spec_class_dict: key=hand, val=specific class
        # ex:{'222': '2_Trips', '223': '2_Pair_Kicker_3', '224': '2_Pair_Kicker_4',.....
        self.spec_class_dict = dict.fromkeys(combos, '')

        # gen_class_dict: key=hand, val=general class
        # ex: {'222': 'Trips', '223': 'Pair w/ Kicker', '224': 'Pair w/ Kicker',...
        self.gen_class_dict = dict.fromkeys(combos, '')

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
            return self.gen_classes[0]
        elif self.is_pair(_hand):
            if _hand[0] == _hand[1]:
                return self.gen_classes[2]
            else:
                return self.gen_classes[1]
        else:
            return self.gen_classes[3]

    def simulate(self):
        for i in range(self.runs):
            random.shuffle(self.deck)
            deal = self.deck[0:3]
            hand = sorted(deal)
            str_hand = [str(z.rank) for z in hand]
            str_hand = ''.join(str_hand)
            self.histo_dict[str_hand] += 1

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

    def results_to_csv(self):
        histo_items = self.histo_dict.items()
        histo_list = list(histo_items)
        df = pd.DataFrame(histo_list)
        current_DT = datetime.datetime.now()
        filename = "guts_histogram_" + str(self.runs) + "_" + str(current_DT.strftime("%m%d_%H_%M")) + ".csv"
        df.to_csv(filename, mode="w", header=False, index=False)
