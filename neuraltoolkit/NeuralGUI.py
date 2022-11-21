import ipywidgets as ipw
from ipywidgets import Tab
from neuraltoolkit.search import drive_search
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



import ipywidgets as ipw
from ipywidgets import AppLayout
from neuraltoolkit.search import drive_search
import os

class _DataScreen(AppLayout):

  def __init__(self):
    self.btn = ipw.Button(description="btn")

    self.path = '/content/drive/MyDrive/'
    self.selected_path = ''
    self.datasets = []
    self.selected_animals = []

    self.path_input = ipw.Text(
    value=self.path if self.path else None,
    placeholder='Path to directory',
    description='Path:',
    style={"description_width":"initial"},
    layout = ipw.Layout(width="90%"),
    disabled=False
    )

    self.search_btn = ipw.Button(
    description='Search',
    disabled=not self.path,
    tooltip='Run Search',
    layout=ipw.Layout(width="10%")
    ) 

    self.header_log = ipw.Output(layout=ipw.Layout(width="auto",
                            height= "100px",
                            max_height="100px",
                            overflow_y="auto",
                            border="1px solid black"))
    
    self.footer_log = ipw.Output(layout=ipw.Layout(width="75%",
                            height= "auto",
                            max_height="52px",
                            display="flex",
                            flex_flow="row",
                            overflow_y="auto",
                            border="1px solid black"))
    
    self.search_header = ipw.VBox([self.header_log, ipw.HBox([self.path_input, self.search_btn])])


    self.dataset_select = ipw.Select(options=self.datasets,
              description="Chosse Dataset",
              style={"description_width":"initial"},
              rows=5,
              layout=ipw.Layout(width="auto", height="100px"),
              value=None)
    
    self.animal_multiselect = ipw.SelectMultiple(
                      options=self.dataset_select.value if self.dataset_select.value else [],
                      description='Chosse animals',
                      layout=ipw.Layout(width="100%", height="auto"),
                      style = {"description_width":"initial"})
    
    self.check_all = ipw.widgets.Checkbox(value=False,
                                 description='Select all',
                                 layout=ipw.Layout(width="80%"),
                                 indent=False)

    self.confirm_btn = ipw.Button(description='Confirm',
                         disabled=False,
                         layout=ipw.Layout(height="50px", width="20%", background_color="white"))
    
    self.footer = ipw.HBox([ipw.Label('Selected Animals', style = {'description_width': 'initial'}), self.footer_log, self.confirm_btn], layout=ipw.Layout(height="auto"),style = {'description_width': 'initial'})

    
    super(_DataScreen, self).__init__(header = self.search_header,
                                      left_sidebar = self.dataset_select,
                                      right_sidebar = ipw.HBox([self.animal_multiselect, self.check_all], layout=ipw.Layout(height="100px")),
                                      footer = self.footer,
                                      grid_gap ="5px",
                                      layout=ipw.Layout(height="auto"),
                                      merge=True,
                                      pane_heights=[3,3,2],
                                      juftify_content="center",
                                      align_items = "center")
    
    self.dataset_select.observe(self.on_dataset_select, names="value")
    self.animal_multiselect.observe(self.on_animal_select, names="value")
    self.search_btn.on_click(self.on_search)
    self.check_all.observe(self.select_all, names="value")
    self.path_input.observe(self.set_path, names='value')
    

  def on_dataset_select(self, change):
    logs = list(change['new'].values())[0]
    path = list(change['new'].keys())[0]
    self.selected_path = path
    self.animal_multiselect.options = {log:os.path.join(path, log) for log in logs}

  def set_path(self, change):
    self.path = change['new']
    if self.path: self.search_btn.disabled = False
    else: self.search_btn.disabled = True


  def on_animal_select(self, change): 
    animals = [x for x in change['new']]
    self.footer_log.clear_output()

    with self.footer_log:
      for animal in animals: print(*animal, sep='', end='\n')


  def on_search(self, btn):
    with self.header_log:
      self.dataset_select.options = []
      # dataset_select.options = drive_search(path_input.value, files=False)
      self.dataset_select.options = {key:{key:value} for key, value in drive_search(self.path_input.value, files=False).items()}
    
        
  def select_all(self, change):
    if change["type"] == 'change':
      if change["new"]: self.animal_multiselect.value = list(self.animal_multiselect.options.values())
      else: self.animal_multiselect.value = []



import ipywidgets as ipw
from ipywidgets import AppLayout
from IPython.display import display
import plotly.express as xp

class _AnalysisScreen(AppLayout):

  def __init__(self):
    self.IFR_out = ipw.Output()
    self.CV_out = ipw.Output()

    self.menu_html = ipw.HTML(value="<h1>Menu:</h1><br>")

    self.ani_dpdw = ipw.Dropdown(options=[], value=None, description='Animal:')

    self.IFR_html = ipw.HTML(value="<h3>IFR:</h3>")
    self.IFR_delta_window = ipw.BoundedFloatText(value=10,
                                                min=0,
                                                max=100.0,
                                                step=0.1,
                                                description='IFR delta:')
    self.IFR_smoothing_coef = ipw.BoundedIntText(value=25,
                                                 min=1,
                                                 max=100,
                                                 step=1,
                                                 description='IFR Smooth Coef:',
                                                 style = {'description_width': 'initial'})

    self.CV_html = ipw.HTML(value="<h3>CV:</h3>")
    self.CV_delta_window = ipw.BoundedIntText(value=10,
                                              min=0,
                                              max=100,
                                              step=1,
                                              description='CV delta:')
    
    self.CV_smoothing_coef = ipw.BoundedIntText(value=25,
                                                min=1,
                                                max=100,
                                                step=1,
                                                description='CV Smooth Coef:',
                                                style = {'description_width': 'initial'})


    self.confirm_btn = ipw.Button(description='Confirm', width='100%')
    self.confirm_btn.on_click(lambda x: self._refresh_views(animal=self.ani_dpdw.value,
                                                               ifr_delta=self.IFR_delta_window.value,
                                                               ifr_smooth_coef=self.IFR_smoothing_coef.value,
                                                               cv_delta=self.CV_delta_window.value,
                                                               cv_smooth_coef=self.IFR_smoothing_coef.value))

    self.menu = ipw.VBox([self.menu_html, self.ani_dpdw,\
                          self.IFR_html, self.IFR_delta_window, self.IFR_smoothing_coef, \
                          self.CV_html, self.CV_delta_window, self.CV_smoothing_coef,\
                          self.confirm_btn], grid_gap="10px", layout=ipw.Layout(width="100%"))
                          
    self.graphs = ipw.VBox(children=[self.IFR_out, self.CV_out], grid_gap="50px")

    super(_AnalysisScreen, self).__init__(left_sidebar=self.menu, right_sidebar=self.graphs,
                       pane_widths=[.75,0,2], justify_content='center', align_items='center')


  def _fig_graph(self, df, title='Title'):
      fig = xp.line(df)

      fig.update_layout(title=title,
                      xaxis_title='Time',
                      yaxis_title='Coef',
                      height=300,)
      return fig

  def _refresh_views(self, **args):
      if not args.get("animal"): return
      animal = args.get("animal")
      self.IFR_out.clear_output()
      self.CV_out.clear_output()
      with self.IFR_out:
        ifr_df = animal.get_IFR_population(binsize=args.get("ifr_delta"), smoothing=args.get("ifr_smooth_coef")).set_index("Hours")
        ifr_fig = self._fig_graph(ifr_df, title=f'{animal.name} IFR')
        display(ifr_fig)
      with self.CV_out:
        cv_df = animal.get_CV_population(binsize=args.get("cv_delta"), smoothing=args.get("cv_smooth_coef")).set_index("Hours")
        cv_fig = self._fig_graph(cv_df, title=f'{animal.name} CV')
        display(cv_fig)

  def clear_graphs(self):
    self.IFR_out.clear_output()
    self.CV_out.clear_output()
