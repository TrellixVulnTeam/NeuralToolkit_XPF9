import ipywidgets as ipw
from ipywidgets import AppLayout
from .search import drive_search
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

