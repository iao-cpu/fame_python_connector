################################################################################
# This program demonstrates how to enable logging
# "chli_log_path" provide file name with path; without path it assumes
#  current working directory
#
# Logging enabled when "chli_log_enable" is set to True
# Logging disabled when "chli_log_enable" is set to False

# Always set "chli_log_enable" after "chli_log_path" is set
################################################################################
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *

try:
    FAMESetProperty("chli_log_path", "generic_connector.log")
    FAMESetProperty("chli_log_enable", "True")
    s0 = FAMEData("chr(126)", "0", "0", 0, "BUSINESS", "down", "Heading", "normal")
    print(s0[1][1])

except OSError as ex:
    print("exception=", ex)