import sys
import pprint
import json
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D

debug = True


def getLabelsAndPayoffs(fname):
    with open(fname, 'r') as f:
        data = json.load(f)

    payoffs = []

    for profile in data["profiles"]:
        elem = []
        for obs in profile["symmetry_groups"]:
            elem.append((obs["role"], obs["strategy"], obs["payoff"]))
        elem.sort()
        payoffs.append(elem)

    if debug:
        pprint.pprint(payoffs)
    return payoffs


def graphPayoffs(payoffs):
    perVsMax = [[], [], []]
    perVsPer = [[], [], []]
    MaxVsPer = [[], [], []]
    MaxVsMax = [[], [], []]
    perVsPCT = [[], [], []]
    MaxVsPCT = [[], [], []]

    for item in payoffs:
        t = []
        for q in zip(item[0], item[1]):
            t.append(q)
        print t
        if "Max" in t[1][1]:
            if "Max" in t[1][0]:
                MaxVsMax[0].append(float(t[1][0].split("-")[1]))
                MaxVsMax[1].append(float(t[1][1].split("-")[1]))
                MaxVsMax[2].append(t[2][1])
            elif "periodic-" in t[1][0]:
                perVsMax[0].append(float(t[1][0].split("-")[1]))
                perVsMax[1].append(float(t[1][1].split("-")[1]))
                perVsMax[2].append(t[2][1])
        elif "periodic-" in t[1][1]:
            if "Max" in t[1][0]:
                MaxVsPer[0].append(float(t[1][0].split("-")[1]))
                MaxVsPer[1].append(float(t[1][1].split("-")[1]))
                MaxVsPer[2].append(t[2][1])
            elif "periodic-" in t[1][0]:
                perVsPer[0].append(float(t[1][0].split("-")[1]))
                perVsPer[1].append(float(t[1][1].split("-")[1]))
                perVsPer[2].append(t[2][1])
        elif "probe" in t[1][0]:
            if "Max" in t[1][0]:
                MaxVsPCT[0].append(float(t[1][0].split("-")[1]))
                MaxVsPCT[1].append(float((
                    t[1][1].split("-")[1].split("-")[0])))
                MaxVsPCT[2].append(t[2][1])
            elif "periodic-" in t[1][0]:
                perVsPCT[0].append(float(t[1][0].split("-")[1]))
                perVsPCT[1].append(float((t[1][1].split("-")[1].split("-")[0])))
                perVsPCT[2].append(t[2][1])

    if debug:
        pprint.pprint(perVsPer)
        pprint.pprint(MaxVsPer)
        pprint.pprint(perVsMax)
        pprint.pprint(MaxVsMax)
        pprint.pprint(perVsPCT)
        pprint.pprint(MaxVsPCT)

    fig = pylab.figure()
    ax = Axes3D(fig)
    pprint.pprint(perVsPer)
    ax.scatter(perVsPer[0], perVsPer[1], perVsPer[2])
    plt.show()

    # plt.scatter(perVsPer[0], perVsPer[1], perVsPer[2])
    # plt.show()


if __name__ == '__main__':
    data = getLabelsAndPayoffs(sys.argv[1])
    graphPayoffs(data)