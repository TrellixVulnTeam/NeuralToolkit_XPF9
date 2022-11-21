from neuraltoolkit.pedros import LocalPopulation
import pandas as pd
import numpy as np
import os, fnmatch


class Animal:

    def __init__(self,logs, name="noname"):
      self.name = name
      path, logs = logs.popitem()

      self._shanks = {log.split('.')[0]: LocalPopulation(os.path.join(path,log), name=log) for log in logs}
    
    def get_shanks(self):
        return self._shanks

    
    def get_CV_population(self, binsize=10, smoothing=25):
      CV_df = pd.DataFrame(columns=['Time'])
      shanks = list(self._shanks.keys())
      for shank, local_population in self._shanks.items():
        CV_series = local_population.CV(bin_size=binsize)
        t, coef = CV_series.index, CV_series.values
        CV_df['Time'] = t
        CV_df[shank] = coef
      
      CV_df["Smoothed Average"] = self._smoothing(CV_df[shanks].apply('mean', axis=1), smoothing)

      CV_df['Hours'] = pd.to_datetime(CV_df.Time, unit='s').dt.strftime('%H:%M:%S')

      return CV_df.drop("Time", axis=1)

    
    def get_IFR_population(self, binsize=10, smoothing=25):
      IFR_df = pd.DataFrame(columns=['Time'])
      shanks = list(self._shanks.keys())
      for shank, local_population in self._shanks.items():
        IFR_series = local_population.IFR(bin_size=binsize)
        t, coef = IFR_series.index, IFR_series.values
        IFR_df['Time'] = t
        IFR_df[shank] = coef

      IFR_df["Smoothed Average"] = self._smoothing(IFR_df[shanks].apply('mean', axis=1), smoothing)
      IFR_df['Hours'] = pd.to_datetime(IFR_df.Time, unit='s').dt.strftime('%H:%M:%S')

      return IFR_df.drop("Time", axis=1)

    
    def _smoothing(self, y, box_pts):
      box = np.ones(box_pts)/box_pts
      s = np.convolve(y, box, mode='same')
      return s

