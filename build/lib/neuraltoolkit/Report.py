import ipywidgets as ipw
from ipywidgets import Tab
from . import Animal, _DataScreen, _AnalysisScreen
from .search import drive_search
import logging.config

class Report(Tab):

  
  def __init__(self):
    self.dataScreen = _DataScreen()
    self.analysisScreen = _AnalysisScreen()
    self._disable_logs()
    super(Report, self).__init__(children=[self.dataScreen,
                                           self.analysisScreen])
    self.set_title(0, "Data")
    self.dataScreen.confirm_btn.on_click(self._confirm_path_data_screen)

    self.set_title(1, 'Analysis')

  def _confirm_path_data_screen(self, btn):
    with self.dataScreen.header_log:
      if not self.dataScreen.animal_multiselect.value or len(self.dataScreen.animal_multiselect.value)==0: print(" No animals selected, please select animals before continue.")
      else: 
        self.dataScreen.selected_animals = self.dataScreen.animal_multiselect.value
        print(f"\033[1;32mAnalysis confirmed on {len(self.dataScreen.selected_animals)} animals.")
        print(f"Fetching data...")
        self.datasets = [drive_search(animal, files=True, verbose=False) for animal in self.dataScreen.selected_animals]
        self.animals = {names[-1]:Animal(d, name=names[-1]) for d in self.datasets for names in [list(d.keys())[0].split('/')]}

        print(f'DONE')

        self.analysisScreen.ani_dpdw.options = self.animals
        self.analysisScreen.clear_graphs()


  
  def _disable_logs(self):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })