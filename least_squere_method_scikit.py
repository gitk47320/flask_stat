# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


clf = LinearRegression()
height = np.array(height)
weight = np.array(weight)
height = height.reshape(-1,1)
weight = weight.reshape(-1,1)

clf.fit(height, weight)

plt.scatter(height, weight)
plt.plot(height,clf.predict(height))
plt.show()