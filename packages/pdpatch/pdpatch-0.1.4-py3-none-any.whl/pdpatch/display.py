# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_display.ipynb.

# %% auto 0
__all__ = ['Walker', 'Less']

# %% ../02_display.ipynb 2
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from fastcore.all import *

from .core import *

# %% ../02_display.ipynb 3
@patch
def title(self:pd.DataFrame, title):
    '''Displays DataFrame with a title.'''
    out = widgets.Output()
    with out: display(self)
    layout = widgets.Layout(align_items='center')
    return widgets.VBox([widgets.Label(title, layout=layout), out])

# %% ../02_display.ipynb 5
class Walker:
    def __init__(self, val=0, min_val=None, max_val=None): store_attr()
    def _next(self, *args, val=1, **kwargs):
        self.val += val
        if self.max_val: self.val = min(self.max_val, self.val)
    def _prev(self, *args, val=1, **kwargs):
        self.val -= val
        if self.min_val: self.val = max(self.min_val, self.val)
    def _head(self):
        self.val = 0
        if self.min_val: self.val = max(self.min_val, self.val)       

# %% ../02_display.ipynb 6
class Less:
    def __init__(self, df, page_size=5, page=1, where=None):
        store_attr()
        if not where is None:
            page = math.floor(L(range_of(df))[where][0]/page_size+1)
            
        self.out = widgets.Output(wait=True)
        self.out_df = widgets.Output(wait=True)
        self.out_df.append_display_data(self.df.page(page, page_size=self.page_size))
        
        self.n_pages = len(df)//self.page_size+1
        self.page = Walker(val=page, min_val=1, max_val=self.n_pages)

        self.next = widgets.Button(description='next')
        self.next.on_click(self.page._next)
        self.next.on_click(self.refresh)

        self.prev = widgets.Button(description='prev')
        self.prev.on_click(self.page._prev)
        self.prev.on_click(self.refresh)
        
        layout = widgets.Layout(width='100%', display='flex', align_items='center')
        self.out_label = widgets.Output(wait=True)
        with self.out_label: display(widgets.Label(f"page {self.page.val} of {self.n_pages}"))
        self.box = widgets.VBox([widgets.HBox([self.prev, self.next, self.out_label]), self.out_df])
        with self.out: 
            display(self.box)

    def refresh(self, event):
        self.out_df.clear_output()
        with self.out_df: display(self.df.page(self.page.val, page_size=self.page_size))
        self.out_label.clear_output()
        with self.out_label: display(widgets.Label(f"page {self.page.val} of {self.n_pages}"))

# %% ../02_display.ipynb 7
@patch
def less(self:pd.DataFrame, page_size=5, page=1, where=None):
    '''Displays one page of the DataFrame and buttons to move forward and backward.'''
    return Less(self, page_size=page_size, page=page, where=where).out

# %% ../02_display.ipynb 10
@patch
def less(self:pd.Series, page_size=5, where=None):
    '''Displays one page of the Series and buttons to move forward and backward.'''
    return Less(self, page_size=page_size, where=where).out

# %% ../02_display.ipynb 12
@patch
def to_percent(self:pd.DataFrame, exclude=[]):
    'Formats float columns to percentage.'
    cols = self.dtypes[self.dtypes=='float'].index
    cols = [c for c in cols if c not in exclude]
    return self.style.format({c: '{:.1%}'.format for c in cols})
