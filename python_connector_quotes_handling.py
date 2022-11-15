################################################################################
# This program demonstrates how to handle in between double quotes in expression
# User needs to guard every in bbetween double quotes with '\' (baclslash sign)
# E.g. If your expression is "datefmt(t,""<year>-<m>-<d>"")"
#      You need to provide like "datefmt(t,\"\"<year>-<m>-<d>\"\")"
################################################################################
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *

try:
    s2 = FAMEData("datefmt(t,\"\"<year>-<m>-<d>\"\")", "2000", "2020", 0,"MONTHLY", "down", "Heading", "normal")
    for data in s2[1]:
        print(data)

except OSError as ex:
    print("exception=", ex)
