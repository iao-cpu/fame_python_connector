################################################################################
# This program demonstrates how to draw simple bar graph
################################################################################
import sys
import math

sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *

import matplotlib.pyplot as plt

try:
    s1 = FAMEData("*$get_list{famedate, euro01.ivl.g, euro02.ivl.g, euro03.ivl.g}", "2017", "2020", 0, "MONTHLY", "down", "Heading",
                  "normal")

    x_axis = []
    y_axis = []
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("A test graph")


    for x, y, z, q in zip((s1[1])[1:], (s1[2])[1:], (s1[3])[1:], (s1[4])[1:]):
        if math.isnan(y):
            continue
        x_axis.append(FAMEConvertToDateTime(x, "%Y-%m-%d"))
        y_axis.append(float("{:.2f}".format(y, z, q)))
    plt.bar(x_axis, y_axis, width=1)
    plt.legend()
    plt.show()

except OSError as ex:
    print("exception=", ex)
