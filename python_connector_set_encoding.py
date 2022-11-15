################################################################################
# This program demonstrates how to set encoding
################################################################################
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *

try:
    FAMESetProperty("encoding", "utf-8")
    s0 = FAMEData("chr(226) + chr(130) + chr(172)", "0", "0", 0, "BUSINESS", "down", "Heading", "normal")
    print(s0[1][1])

except OSError as ex:
    print("exception=", ex)
