### This program demonstarates how to get data from fame database
### and plot graph with it
### This program also demonstrates how to change date formatting.
### Default is whatever stored in series (depends on frequency)
### Plese refer fame help for supported formats
### This program uses uses local database connection to connect to fame database
### User needs to change database location in below program as per his fame installation
import sys
import math
sys.path.insert(0, '..')
sys.path.insert(0, '.')
from fame_connector import *
import matplotlib.pyplot as plt
from datetime import datetime


hostname = ""
service = ""
username = ""
password = ""
attr = {'dateformat':"<MTXTL> <YZ>"}

#sdata = FAMEData("*$get_list{famedate, euro01.ivl.g}", "2010", "2017", 0, "MONTHLY", "down", "Heading","normal")

sdata1 = getobjectbyname(service, hostname, username, password, "C:\\Projects\\FAME116\\util\\training.db", "ibm.open", attr)
x_axis = []
y_axis = []
#plt.xlabel("X-axis")
#plt.ylabel("Y-axis")
#plt.title("A test graph")

for x, y in zip((sdata[1])[1:], (sdata[2])[1:]):
    if math.isnan(y):
        continue
    print(x, float("{:.2f}".format(y)))
    x_axis.append(FAMEConvertToDateTime(x, "%Y-%m-%d"))
    y_axis.append(float("{:.2f}".format(y)))

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.spines['bottom'].set_color('blue')
ax.spines['left'].set_color('red')
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_color(None)
ax.spines['top'].set_color(None)
ax.set_xlabel("Date")
ax.set_ylabel("price")
ax.bar(x_axis, y_axis)
plt.legend()
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("A test graph")
plt.show()
