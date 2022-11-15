################################################################################
# This program demonstrates how to draw simple line graph
################################################################################
import sys
import math
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *
import matplotlib.pyplot as plt

try:
    s1 = FAMEData("*$get_list{famedate, euro01.ivl.g, euro02.ivl.g, euro03.ivl.g}", "2010", "2017", 0, "MONTHLY", "down", "Heading",
                  "normal")

    #fig = plt.figure()
    #fig = plt.subplots(figsize=(12, 12))
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("A test line graph")

    x_axis = []
    y_axis = []

    for x, y in zip((s1[1])[1:], (s1[2])[1:]):
        if math.isnan(y):
            continue
        x_axis.append(FAMEConvertToDateTime(x, "%Y-%m-%d"))
        y_axis.append(float("{:.2f}".format(y)))

    plt.plot(x_axis, y_axis, color='purple')
    plt.legend()
    plt.show()

except OSError as ex:
    print("exception=", ex)
