import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import json

with open("aeMap.json") as f:
    data = json.load(f)
data = data['routes']
# miller projection 
map = Basemap(projection='mill')
for route in data:
    try:
        map.drawgreatcircle(
            route['city1']['longitude'],
            route['city1']['latitude'],
            route['city2']['longitude'],
            route['city2']['latitude'],
            linewidth=1,
            color='b'
        )
    except:
        pass
map.bluemarble()
# map.drawcoastlines()
plt.show()
