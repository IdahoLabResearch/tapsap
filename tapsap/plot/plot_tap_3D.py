# plot_tap_3D
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import plotly.express as px
import numpy as np
import pandas as pd

def plot_tap_3D(x: np.ndarray, y: np.ndarray, z:np.ndarray, save_path: str = None, x_lab: str = 'Time (s)', y_lab: str = 'Flux (V)', z_lab:str = 'Z', font_size: float = 30, legend: bool = False, min_max_x_tick:list = None, min_max_y_tick:list = None, min_max_z_tick:list) -> list:
    """

    This function leverages plotly for plotting flux information.
    Note that in some cases, the amount of information to plot may be large and will increase the time to plot.
    The values for x and y may be either an 1d numpy array or a DataFrame.
    If there is a mismatch of shapes between the data, then the smallest array will be repeated to match the larger.

    
    Args:
        x (ndarray | DataFrame): This can be either a 1d numpy array or a DataFrame. If 1d, then the values will be repeated by the shape of information in y.

        y (ndarray | DataFrame): This can be either a 1d numpy array or a DataFrame. If 1d, then the values will be repeated by the shape of information in x.

        z (ndarray | DataFrame): This can be either a 1d numpy array or a DataFrame. If 1d, then the values will be repeated by the shape of information in x.

        save_path (str): A string path, e.g., plots/flux_results.png, where an image can be saved.

        x_lab (str): The value of the x label axis.

        y_lab (str): The value of the y label axis.

        z_lab (str): The value of the z label axis.

        font_size (int): The font size of the plot.

        legend (bool): A boolean indicator to plot the legend or not.

        min_max_x_tick (list): A start, stop, and length of the x ticks.

        min_max_y_tick (list): A start, stop, and length of the y ticks.

        min_max_z_tick (list): A start, stop, and length of the z ticks.

    Returns:
        fig (plotly.express): The plotly figure if the save_path is not none.  Can be shown using fig.show().

    Citation:
        None

    Implementor:
        M. Ross Kunz

    Link:
        None

    """
    # plot setup
    colors = None

    if isinstance(x, pd.DataFrame):
        colors_x = np.repeat(np.array(list(x.columns)), x.shape[0])
        x = np.array(x).transpose().flatten()

    if isinstance(y, pd.DataFrame):
        colors_y = np.repeat(np.array(list(y.columns)), y.shape[0])
        y = np.array(y).transpose().flatten()

    if isinstance(z, pd.DataFrame):
        colors_z = np.repeat(np.array(list(z.columns)), z.shape[0])
        z = np.array(z).transpose().flatten()

    all_lens = np.array([len(x), len(y), len(z)])
    
    max_index = np.argmax(all_lens)
    max_len = max(all_lens)

    if len(x) < max_len:
        max_repeating = int(np.ceil(max_len / len(x)))
        x = np.array(list(x) * max_repeating)[0:max_len]

    if len(y) < max_len:
        max_repeating = int(np.ceil(max_len / len(y)))
        y = np.array(list(y) * max_repeating)[0:max_len]

    if len(z) < max_len:
        max_repeating = int(np.ceil(max_len / len(z)))
        z = np.array(list(z) * max_repeating)[0:max_len]

    if max_index == 0:
        colors = colors_x
    elif max_index == 1:
        colors = colors_y
    else:
        colors = colors_z
        

    temp_dict = {
        'x': x,
        'y': y,
        'z': z,
        'colors': colors
    }
    df = pd.DataFrame(data=temp_dict)
    fig = px.line_3d(df, x='x', y='y', z='z', template='plotly_white')

    if min_max_x_tick is None:
        x_range = [np.floor(x), np.ceil(x)]
        x_tick_vals = np.arange(x_range[0], x_range[1], 5)
    else:
        x_range = [min_max_x_tick[0], min_max_x_tick[1]]
        x_tick_vals = np.arange(x_range[0], x_range[1], min_max_x_tick[2])

    if min_max_y_tick is None:
        y_range = [np.floor(y), np.ceil(y)]
        y_tick_vals = np.arange(y_range[0], y_range[1], 5)
    else:
        y_range = [min_max_y_tick[0], min_max_y_tick[1]]
        y_tick_vals = np.arange(y_range[0], y_range[1], min_max_y_tick[2])

    if min_max_z_tick is None:
        z_range = [np.floor(z), np.ceil(z)]
        z_tick_vals = np.arange(z_range[0], z_range[1], 5)
    else:
        z_range = [min_max_z_tick[0], min_max_z_tick[1]]
        z_tick_vals = np.arange(z_range[0], z_range[1], min_max_z_tick[2])


    tick_size = 16
    label_size = 20 
    x_info = dict(
        title = x_lab,
        range = x_range,
        tickvals = x_tick_vals,
        tickfont = dict(size = tick_size),
        titlefont = dict(size = label_size),
        tickangle = -30,
        autorange = "reversed"#,
        #ticksuffix = x_suffix
    )
    y_info = dict(
        title = y_lab,
        range = y_range,
        tickvals = y_tick_vals,
        tickfont = dict(size = tick_size),
        titlefont = dict(size = label_size),
        tickangle = -30,
        #exponentformat = "e",
        automargin=True#,
        #tickprefix = '\uFE52   '#, # '\uFE52        ',
        #ticksuffix = 'm'
    )
    z_info = dict(
        title = z_lab,
        range = z_range,
        tickvals = z_tick_vals,
        tickfont = dict(size = tick_size),
        titlefont = dict(size = label_size),
        tickangle = -30,
        #exponentformat = "e",
        automargin=True#,
        #tickprefix = '\uFE52   '#, # '\uFE52        ',
        #ticksuffix = 'm'
    )

    m = dict(l=15, r=20, b=10, t=10)
    fig.update_layout(
      margin=m,
      scene = dict(
        xaxis = x_info,
        yaxis = y_info,
        zaxis = z_info,
        camera = dict(
          eye = dict(x = 1.3, y = 1.3, z = .001),
          center = dict(x = 0, y = 0, z = -.1))
    ))
    fig.update_traces(showscale=False)

    if save_path is not None:
        fig.write_image(save_path)
    else:
        return fig
