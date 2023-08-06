# -*- coding: utf-8 -*-


"""
Created on Nov 2018

Samle comparing different models

@author: guillaume
"""
from __future__ import print_function

import pandas as pd
import matplotlib.pyplot as plt
from agmodeling.scoring.set_method import get_IPI_score


file = "sample_data.xlsx"
print("Read excel data file : %s" % file)
df = pd.read_excel(file)
print("containing %d data " % df.size)
# print df.head()
df25 = df.filter(regex=".*25.*")
df25.plot()
df10 = df.filter(regex=".*10.*")
df10.plot()

results = dict()

listModelNames = list()
for col in df10.columns:
    print(col)
    modelName = col.split("_", 1)[1]
    if modelName != "REF":
        listModelNames.append(modelName)


PM25 = "PM25"
PM10 = "PM10"

results25 = list()
datas = dict()
datas[PM25] = list()
for col in df25.columns:
    if col != "PM25_REF":
        print("\nScore IPI for %s" % col)
        ipi = get_IPI_score(df["PM25_REF"], df[col])
        datas[PM25].append(ipi)

datas[PM10] = list()
for col in df10.columns:
    if col != "PM10_REF":
        print("\nScore IPI for %s" % col)
        ipi = get_IPI_score(df["PM10_REF"], df[col])
        datas[PM10].append(ipi)

res = pd.DataFrame.from_dict(datas, orient="index")
res.columns = listModelNames

print("\n========================================")
print("Results :")
print(res)


print("\nFin du programme")
plt.show()
