#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire, warnings
from datetime import datetime

class Regbot:
  reg_model_path = resource_filename(__name__, 'finalized_model.h5') 
  model_scaler_path = resource_filename(__name__, 'logscaler.gz') 
  thr = 0.5048710627477806 # remember to change this value for every model

  def __init__(self,*args):
  	pass



  @classmethod  
  def loadmodel(cls):
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      loaded_model = joblib.load(open(f'{cls.reg_model_path}', 'rb'))
      return loaded_model
  @classmethod
  def getWeekDay(cls,utcdatetime):
      date = datetime.fromisoformat(utcdatetime)
      day = date.isoweekday()
      return day
  
  @classmethod
  def getUtcHour(cls, utcdatetime):
      utchour = int(str(utcdatetime).split(' ')[1].split(':')[0])
      return utchour

  @classmethod  
  def prepareInput(cls,opening,closing,utcdatetime):
    avr = closing/(opening + closing)
    bvr = opening/(opening + closing)
    day = cls.getWeekDay(utcdatetime)
    time = cls.getUtcHour(utcdatetime)  
    testdata = np.array([[avr,bvr,day,time]])
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      scaler = joblib.load(f'{cls.model_scaler_path}')
      testdata = scaler.transform(testdata)

      return testdata


  @classmethod
  def shortSignalGenerator(cls,opening,closing,utcdatetime):
    scalledInput = cls.prepareInput(opening,closing,utcdatetime)
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      return (cls.loadmodel().predict_proba(scalledInput)[:,1] > cls.thr).astype(int)[0]
    
  @classmethod
  def longSignalGenerator(cls,opening,closing,utctime):
    scalledInput = cls.prepareInput(opening,closing,utctime)
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      return (cls.loadmodel().predict_proba(scalledInput)[:,1] <= cls.thr).astype(int)[0]




def signal(opening: float,
          closing: float,
          utcdatetime: str,
          dir: str
          ):
  if dir == 'long':
    try:
      return Regbot.longSignalGenerator(opening,closing,utcdatetime)
    except Exception as e:
      print(e)
  if dir == 'short':
    try:
      return Regbot.shortSignalGenerator(opening,closing,utcdatetime)
    except Exception as e:
      print(e)
  else:
    print(f'{dir} is not a valid direction')
    return

if __name__ == '__main__':
  fire.Fire(signal)
