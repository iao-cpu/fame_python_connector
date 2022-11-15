### This program demonstarates how to get data from fame database
### and plot graph with it
###
### This program uses uses local database connection to connect to fame database
### User needs to change database location in below program as per his fame installation
import pandas as pd
#from printobjects import *
from fame_connector.py import *
import matplotlib.pyplot as plt
from datetime import datetime

hostname = ""
service = ""
username = ""
password = ""

sdata = getobjectbyname(service, hostname, username, password, "C:\\famedb\\detoms.db",  "euro01.ivl.g", None)
#data = pd.read_csv("c:\\python_connector\euro_01.csv", usecols=['Date','euro01.ivl.g'],parse_dates=['Date'],
                                            # index_col=['Date'] )

#sdata1 = getobjectbyname(service, hostname, username, password, "C:\\famedb\\detoms.db",  "euro02.ivl.g", None)

x_axis = []
y_axis = []
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("A test graph")

for x, y in sdata:
    if math.isnan(y):
        continue
    #print(datetime.strptime(x, '%d%b%Y').date(), "       ", float("{:.2f}".format(y)))
    #x_axis.append(datetime.strptime(x, '%d%b%Y').date())
    print(x,float("{:.2f}".format(y)))
    x_axis.append(datetime.strptime(x, '%b%Y').date())
    y_axis.append(float("{:.2f}".format(y)))

""" for x, y in sdata:
    if math.isnan(y):
        continue
    #print(datetime.strptime(x, '%d%b%Y').date(), "       ", float("{:.2f}".format(y)))
    #x_axis.append(datetime.strptime(x, '%d%b%Y').date())
    print(x,float("{:.2f}".format(y)))
    x_axis.append(datetime.strptime(x, '%b%Y').date())
    y_axis.append(float("{:.2f}".format(y))) """

#fig, ax = plt.subplots(figsize=(10, 7))
#data.plot(kind='bar', ax=ax)
#plt.plot(data)

plt.plot(x_axis, y_axis, label='date numeric')
#plt.plot(kind='bar', x_axis, y_axis, label='date numeric')

plt.legend()
plt.show()