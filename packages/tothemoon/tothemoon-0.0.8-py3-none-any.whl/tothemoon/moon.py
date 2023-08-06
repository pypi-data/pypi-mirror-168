#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire


class Regbot:
  reg_model_path = resource_filename(__name__, 'btc_model.h5') 
  model_scaler_path = resource_filename(__name__, 'btclogscaler.gz') 
  thr = 0.6270420075454726

  def __init__(self,*args):
  	pass



  @classmethod  
  def loadmodel(cls):
    loaded_model = joblib.load(open(f'{cls.reg_model_path}', 'rb'))
    return loaded_model

  @classmethod
  def getUtcHour(cls,utcdatetime):
    return str(utcdatetime).split(' ')[1][1]

  @classmethod  
  def prepareInput(cls,opening,closing,utcdatetime):
    avr = closing/(opening + closing)
    bvr = opening/(opening + closing)
    utctime = cls.getUtcHour(utcdatetime)
    testdata = np.array([[avr,bvr,utctime]])
    scaler = joblib.load(f'{cls.model_scaler_path}')
    testdata = scaler.transform(testdata)

    return testdata


  @classmethod
  def buySignalGenerator(cls,opening,closing,utcdatetime):
    scalledInput = cls.prepareInput(opening,closing,utcdatetime)
    return np.round(np.clip(cls.loadmodel().predict(scalledInput), 0, cls.thr) > 0)[0].astype(int)





def signal(opening, closing,utcdatetime):
  try:
    return Regbot.buySignalGenerator(opening,closing,utcdatetime)
  except Exception as e:
    print(e)


if __name__ == '__main__':
  fire.Fire(signal)
