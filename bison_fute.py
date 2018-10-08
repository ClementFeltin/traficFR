import requests
import numpy as np
import pandas as pd
import json
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

# Downloading data from Bison Futé
link = "http://www.bison-fute.gouv.fr/previsions/previsions.json"
req = requests.get(link)
data_json = req.json()

# Dumping downloaded json to file
with open("data_file" + timestr + ".json", "w") as write_file:
    json.dump(data_json, write_file)

# Preprocessing data
list = []

for list_i in data_json["values"]:
    list_dept = []
    for couple in list_i:
        list_couple = couple.split(",")
        list_dept.append(list_couple)

    list_dept = list_dept[0:94]
    list.append(list_dept)

array = np.transpose(np.array(list), [1,0,2])

# Creating Pandas Panel
panel = pd.Panel(array,items=data_json["deptsLine"][0:94],
                 major_axis=data_json["days"],
                 minor_axis=["depart", "retour"])

# Creating and formating multiindex dataframe
frame = panel.to_frame()
frame.index.names = ["dates", "direction"]
frame.columns.name = "departement"