# plot_tap
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import plotly.express as px
import numpy as np
import pandas as pd

def plot_tap(x: np.ndarray, y: np.ndarray, y_names: list = None, save_path: str = None, x_lab: str = 'Time (s)', y_lab: str = 'Flux (V)', font_size: float = 30, legend: bool = False,min_max_x_tick:list = None, min_max_y_tick:list = None) -> list:
    """

    This function leverages plotly for plotting flux information.
    Note that in some cases, the amount of information to plot may be large and will increase the time to plot.
    The values for x and y may be either an 1d numpy array or a DataFrame.
    If there is a mismatch of shapes between the data, then the smallest array will be repeated to match the larger.

    
    Args:
        x (ndarray | DataFrame): This can be either a 1d numpy array or a DataFrame. If 1d, then the values will be repeated by the max shape of information.

        y (ndarray | DataFrame): This can be either a 1d numpy array or a DataFrame. If 1d, then the values will be repeated by the max shape of information.

        y_names (str list): A list of specific column names to plot in the data frame.

        save_path (str): A string path, e.g., plots/flux_results.png, where an image can be saved.

        x_lab (str): The value of the x label axis.

        y_lab (str): The value of the y label axis.

        z_lab (str): The value of the z label axis.

        font_size (int): The font size of the plot.

        legend (bool): A boolean indicator to plot the legend or not.

        min_max_x_tick (list): A start, stop and length of the x ticks.

        min_max_y_tick (list): A start, stop and length of the x ticks.


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
    if isinstance(y, pd.DataFrame):
        if y_names is None:
            colors = np.repeat(np.array(list(y.columns)), y.shape[0])
            y = np.array(y).transpose().flatten()
        else:
            colors = np.repeat(np.array(list(y_names)), y.shape[0])
            y = np.array(y[y_names]).transpose().flatten()

    if isinstance(x, pd.DataFrame):
        x = np.array(x).transpose().flatten()

    max_len = max([len(y), len(x)])

    if len(y) < max_len:
        max_repeating = int(np.ceil(max_len/ len(y)))
        y = np.array(list(y) * max_repeating)[0:max_len]
        colors = np.array(list(colors) * max_repeating)[0:max_len]

    if len(x) < max_len:
        max_repeating = int(np.ceil(max_len/ len(x)))
        x = np.array(list(x) * max_repeating)[0:max_len]

    if colors is not None:
        temp_dict = {
            'x': x,
            'y': y,
            'colors': colors
        }
        df = pd.DataFrame(data=temp_dict)
        fig = px.line(df, x='x', y='y', color='colors',
                      template='plotly_white')
    else:
        temp_dict = {
            'x': x,
            'y': y
        }
        df = pd.DataFrame(data=temp_dict)
        fig = px.line(df, x='x', y='y', template='plotly_white')

    fig.update_layout(
        showlegend=legend,
        xaxis_title=x_lab,
        yaxis_title=y_lab,
        legend_title='Index',
        font={
            'size': font_size
        }
    )

    fig.update_layout(legend_font_size=20)

    if min_max_x_tick is not None:
        temp_range = list(np.linspace(min_max_x_tick[0], min_max_x_tick[1], num = min_max_x_tick[2]))
        fig.update_xaxes(tickvals=temp_range)

    if min_max_y_tick is not None:
        temp_range = list(np.linspace(min_max_y_tick[0], min_max_y_tick[1], num = min_max_y_tick[2]))
        fig.update_yaxes(tickvals=temp_range)

    fig.update_layout(legend=dict(
        orientation = 'h',
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=.99
    ))
    fig.update_layout(legend_title_text='', width = 1500, height = 500)


    if save_path is not None:
        fig.write_image(save_path)
    else:
        return fig
