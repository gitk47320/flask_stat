import imp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import common as cmn
from sklearn.linear_model import LinearRegression
matplotlib.use('Agg')
from io import BytesIO
from flask import send_file
import mpld3
from mpld3 import plugins

IMGSAVE_DIR = 'C:\\Users\\junya\\source\\repos\\flask_stat\\templates'

def stserveLinearRegression(filename,imgfilename):
  expvar,objvar = cmn.stservecsv2numpy(filename)
  #print(expvar,objvar)
  expvar_n,objvar_n = cmn.stservenormalization(expvar,objvar)
  clf = LinearRegression()
  fitresult = clf.fit(expvar_n,objvar_n)
  plt.scatter(expvar_n,objvar_n)
  plt.plot(expvar_n,fitresult.predict(expvar_n))
  plt.savefig(imgfilename,format='png')
  image = cmn.stserveencode64(imgfilename)
  return fitresult,image