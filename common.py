import os
import werkzeug
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import Flask, request, make_response, jsonify
import string
import base64


def stservecsv2numpy(filename):
  data = np.loadtxt(filename,delimiter=",",skiprows=1)
  expvar = np.array(data[:,0])
  objvar = np.array(data[:,1])
  return expvar,objvar

def stservenormalization(expvar, objvar):
  expvar_n = expvar.reshape(-1,1)
  objvar_n = objvar.reshape(-1,1)
  return expvar_n,objvar_n

def stserveencode64(filename):
  img = open(filename, 'rb')
  data = base64.b64encode(img.read())
  img.close()
  return "data:image/png;base64," + data.decode('utf-8')