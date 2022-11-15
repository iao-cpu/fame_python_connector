################################################################################
# This program demonstrates how print data in row column format
################################################################################
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *

def printrowcolumns(*dictdata):
    for k in range(1, len(*dictdata) + 1, 1):
        print(dictdata[0][k][0])

    for x in zip(*dictdata):
        print(x)

try:
    s1 = FAMEData("*$get_list{famedate, euro01.ivl.g, euro02.ivl.g, euro03.ivl.g}", "2000", "2017", 10, "MONTHLY", "down", "Heading",
                  "normal")
    # print header as you have given "Heading". Comment below lnine if you have given "No heading" or just "N"
    for k in range(1, len(s1) + 1, 1):
        print(s1[k][0], end =" ")

    # three variable as get_list has three items in above FameData()
    # Since we have printed header above lets get rid of first element
    for x, y, z in zip(s1[1][1:], s1[2][1:], s1[3][1:]):
        print(FAMEConvertToDateTime(x, "%Y-%m-%d"), y, z)

except OSError as ex:
    print("exception=", ex)
