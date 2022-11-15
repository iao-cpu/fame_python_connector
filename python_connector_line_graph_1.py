################################################################################
# This program demonstrates how to draw simple line graph
################################################################################
import sys
import math
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy

try:
    #s1 = FAMEData("*$get_list{famedate, fis.open}", "2000", "2020", 0, "m", "down", "Heading",
                 # "normal")
    s1 = FAMEData("*$get_list{famedate, euro01.ivl.g, euro02.ivl.g, euro03.ivl.g}", "2000", "2020", 0, "m", "down", "Heading",
     "normal")

    plt.xlabel("Date")
    plt.ylabel("Omsetning")
    plt.title("A test line graph")
    x_axis = []
    y_axis = []
    w_axis = []
    z_axis = []
    #a interval parameter set for x- axis
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))

    for x, y, w, z in zip((s1[1])[1:], (s1[2])[1:], s1[3][1:], s1[4][1:]):
        if math.isnan(y):
            continue
        x_axis.append(FAMEConvertToDateTime(x, "%Y-%m-%d"))
        y_axis.append(float("{:.2f}".format(y)))
        #x_axis.append(FAMEConvertToDateTime(x, "%Y-%m-%d"))
        w_axis.append(float("{:.2f}".format(w)))
        z_axis.append(float("{:.2f}".format(z)))

    plt.plot(x_axis, y_axis, label="euro01.ivl.g")
    plt.plot(x_axis, w_axis, label="euro02.ivl.g")
    plt.plot(x_axis, z_axis, label="euro03.ivl.g")
    plt.gcf().autofmt_xdate()
    plt.legend(loc="upper left")
    plt.savefig("C:\\python_connector\png\\myfig1.jpg")

    # Create Table/csv
    print(x_axis, y_axis)



    # plt.plot(x, y_2, '--', color="#999999", label="$y=x^2$")
    # plt.plot(x, y_3, '-', color="#aaaaaa", label="$y=e^{3/2x}$")  # TODO: Fix the notation here
    # plt.legend(loc="upper left")
    plt.show()

except OSError as ex:
    print("exception=", ex)
