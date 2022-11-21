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
