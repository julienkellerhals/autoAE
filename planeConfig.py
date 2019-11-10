import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

flightRequestDf = pd.read_csv("flightRequest.csv", sep=';')

flightAll = flightRequestDf['depAirport'].loc[flightRequestDf['flightDemandF'] != 0] + ' - ' + flightRequestDf['arrAirport'].loc[flightRequestDf['flightDemandF'] != 0]
flightDemandFAll = (flightRequestDf['flightDemandF'].loc[flightRequestDf['flightDemandF'] != 0] / (flightRequestDf['flightDemandF'] + flightRequestDf['flightDemandC'] + flightRequestDf['flightDemandY']) * 100).dropna()
flightDemandCAll = (flightRequestDf['flightDemandC'].loc[flightRequestDf['flightDemandF'] != 0] / (flightRequestDf['flightDemandF'] + flightRequestDf['flightDemandC'] + flightRequestDf['flightDemandY']) * 100).dropna()
flightDemandYAll = (flightRequestDf['flightDemandY'].loc[flightRequestDf['flightDemandF'] != 0] / (flightRequestDf['flightDemandF'] + flightRequestDf['flightDemandC'] + flightRequestDf['flightDemandY']) * 100).dropna()

flight = flightRequestDf['depAirport'].loc[flightRequestDf['flightDemandF'] == 0] + ' - ' + flightRequestDf['arrAirport'].loc[flightRequestDf['flightDemandF'] == 0]
flightDemandC = (flightRequestDf['flightDemandC'].loc[flightRequestDf['flightDemandF'] == 0] / (flightRequestDf['flightDemandF'] + flightRequestDf['flightDemandC'] + flightRequestDf['flightDemandY']) * 100).dropna()
flightDemandY = (flightRequestDf['flightDemandY'].loc[flightRequestDf['flightDemandF'] == 0] / (flightRequestDf['flightDemandF'] + flightRequestDf['flightDemandC'] + flightRequestDf['flightDemandY']) * 100).dropna()

# Create plot
fig = plt.figure()
plt.subplot(121)
plt.scatter(flightAll, flightDemandFAll, label="First - avg demand: {}".format(round(flightDemandFAll.mean(),2)))
plt.scatter(flightAll, flightDemandCAll, label="Business - avg demand: {}".format(round(flightDemandCAll.mean(),2)))
plt.scatter(flightAll, flightDemandYAll, label="Economy - avg demand: {}".format(round(flightDemandYAll.mean(),2)))
plt.axhline(y=flightDemandFAll.mean(), linestyle='-')
plt.axhline(y=flightDemandCAll.mean(), linestyle='-')
plt.axhline(y=flightDemandYAll.mean(), linestyle='-')
frame1 = plt.gca()
frame1.axes.set_ylim([0, 100])
frame1.axes.get_xaxis().set_visible(False)
plt.legend()


plt.subplot(122)
plt.scatter(flight, flightDemandC, label="Business - avg demand: {}".format(round(flightDemandC.mean(),2)))
plt.scatter(flight, flightDemandY, label="Economy - avg demand: {}".format(round(flightDemandY.mean(),2)))
plt.axhline(y=flightDemandC.mean(), linestyle='-')
plt.axhline(y=flightDemandY.mean(), linestyle='-')
frame2 = plt.gca()
frame2.axes.set_ylim([0, 100])
frame2.axes.get_xaxis().set_visible(False)
plt.legend()

plt.show()

print()
