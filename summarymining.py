import json
import sys
import pprint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

debug = True


def getLabelsAndPayoffs(fname):
    with open(fname, 'r') as f:
        data = json.load(f)

    payoffs = {
        "ATT": [],
        "DEF": []
    }

    for profile in data["profiles"]:
        for obs in profile["symmetry_groups"]:
            payoffs[obs["role"]].append((obs["strategy"], obs["payoff"]))

    if debug:
        for k, v in payoffs.iteritems():
            print k,
            pprint.pprint(v)


def plotGraph(payoffs):
    periodic = []
    periodicMax = []
    probeCountTime = []

    for item in payoffs["ATT"]:
        params = item[0].split('-')
        


if __name__ == '__main__':
    getLabelsAndPayoffs(sys.argv[1])
