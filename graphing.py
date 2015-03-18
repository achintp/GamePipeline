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
    perVsMax = [[], [], [], []]
    perVsPer = [[], [], [], []]
    MaxVsPer = [[], [], [], []]
    MaxVsMax = [[], [], [], []]
    perVsPCT = [[], [], [], []]
    MaxVsPCT = [[], [], [], []]

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
                MaxVsMax[3].append(t[2][0])
            elif "periodic-" in t[1][0]:
                perVsMax[0].append(float(t[1][0].split("-")[1]))
                perVsMax[1].append(float(t[1][1].split("-")[1]))
                perVsMax[2].append(t[2][1])
                perVsMax[3].append(t[2][0])
        elif "periodic-" in t[1][1]:
            if "Max" in t[1][0]:
                MaxVsPer[0].append(float(t[1][0].split("-")[1]))
                MaxVsPer[1].append(float(t[1][1].split("-")[1]))
                MaxVsPer[2].append(t[2][1])
                MaxVsPer[3].append(t[2][0])
            elif "periodic-" in t[1][0]:
                perVsPer[0].append(float(t[1][0].split("-")[1]))
                perVsPer[1].append(float(t[1][1].split("-")[1]))
                perVsPer[2].append(t[2][1])
                perVsPer[3].append(t[2][0])
        elif "probe" in t[1][1]:
            if "Max" in t[1][0]:
                MaxVsPCT[0].append(float(t[1][0].split("-")[1]))
                MaxVsPCT[1].append(float((
                    t[1][1].split("-")[1].split("_")[0])))
                MaxVsPCT[2].append(t[2][1])
                MaxVsPCT[3].append(t[2][0])
            elif "periodic-" in t[1][0]:
                perVsPCT[0].append(float(t[1][0].split("-")[1]))
                perVsPCT[1].append(float((
                    t[1][1].split("-")[1].split("_")[0])))
                perVsPCT[2].append(t[2][1])
                perVsPCT[3].append(t[2][0])

    if debug:
        pprint.pprint(perVsPer)
        pprint.pprint(MaxVsPer)
        pprint.pprint(perVsMax)
        pprint.pprint(MaxVsMax)
        pprint.pprint(perVsPCT)
        pprint.pprint(MaxVsPCT)

    fig = pylab.figure()
    ax = Axes3D(fig)
    # pprint.pprint(perVsPer)
    ax.plot(perVsPer[0], perVsPer[1], perVsPer[2], c='r')
    ax.plot(perVsMax[0], perVsMax[1], perVsMax[2], c='r')
    ax.plot(MaxVsPer[0], MaxVsPer[1], MaxVsPer[2], c='r')
    ax.plot(MaxVsMax[0], MaxVsMax[1], MaxVsMax[2], c='r')
    ax.plot(perVsPer[0], perVsPer[1], perVsPer[3], c='b')
    ax.plot(perVsMax[0], perVsMax[1], perVsMax[3], c='b')
    ax.plot(MaxVsPer[0], MaxVsPer[1], MaxVsPer[3], c='b')
    ax.plot(MaxVsMax[0], MaxVsMax[1], MaxVsMax[3], c='b')

    plt.show()

    fig = pylab.figure()
    ax = Axes3D(fig)
    ax.plot(MaxVsPCT[0], MaxVsPCT[1], MaxVsPCT[2], c='r')
    ax.plot(perVsPCT[0], perVsPCT[1], perVsPCT[2], c='r')
    ax.plot(MaxVsPCT[0], MaxVsPCT[1], MaxVsPCT[3], c='b')
    ax.plot(perVsPCT[0], perVsPCT[1], perVsPCT[3], c='b')

    plt.show()

    # plt.scatter(perVsPer[0], perVsPer[1], perVsPer[2])
    # plt.show()


if __name__ == '__main__':
    data = getLabelsAndPayoffs(sys.argv[1])
    graphPayoffs(data)