#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting utilities, leveraging Matplotlib.
"""

__all__ = ['set_style','closefig', 'savefig']


import matplotlib.pyplot as plt
import pathlib
import matplotlib as mpl


def scatter_xy(x,y,c=None, figsize=None, xlabel=None, ylabel=None, title=None, 
            xlim=None, ylim=None, savefig_settings=None, ax=None,
            legend=True, plot_kwargs=None, lgd_kwargs=None):
    """
    Make scatter plot. 

    Parameters
    ----------
    x : numpy.array
        x value
    y : numpy.array
        y value
    c : TYPE, optional
        DESCRIPTION. The default is None.
    figsize : list, optional
        A list of two integers indicating the dimension of the figure. The default is None.
    xlabel : str, optional
        x-axis label. The default is None.
    ylabel : str, optional
        y-axis label. The default is None.
    title : str, optional
        Title for the plot. The default is None.
    xlim : list, optional
        Limits for the x-axis. The default is None.
    ylim : list, optional
        Limits for the y-axis. The default is None.
    savefig_settings : dict, optional
        the dictionary of arguments for plt.savefig(); some notes below:
        - "path" must be specified; it can be any existed or non-existed path,
          with or without a suffix; if the suffix is not given in "path", it will follow "format"
        - "format" can be one of {"pdf", "eps", "png", "ps"}
       The default is None.
    ax : pyplot.axis, optional
        The axis object. The default is None.
    legend : bool, optional
        Whether to include a legend. The default is True.
    plot_kwargs : dict, optional
        the keyword arguments for ax.plot(). The default is None.
    lgd_kwargs : dict, optional
        the keyword arguments for ax.legend(). The default is None.

    Returns
    -------
    ax : the pyplot.axis object

    """
    savefig_settings = {} if savefig_settings is None else savefig_settings.copy()
    plot_kwargs = {} if plot_kwargs is None else plot_kwargs.copy()
    lgd_kwargs = {} if lgd_kwargs is None else lgd_kwargs.copy()
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(x, y, c=c, **plot_kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if title is not None:
        ax.set_title(title)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    if legend:
        ax.legend(**lgd_kwargs)
    else:
        ax.legend().remove()

    if 'fig' in locals():
        if 'path' in savefig_settings:
            savefig(fig, settings=savefig_settings)
        return fig, ax
    else:
        return ax


def plot_scatter_xy(x1,y1,x2,y2, figsize=None, xlabel=None,
                    ylabel=None, title=None, xlim=None, ylim=None,
                    savefig_settings=None, ax=None, legend=True, 
                    plot_kwargs=None, lgd_kwargs=None):
    
    ''' Plot a scatter on top of a line plot.
    
    Parameters
    ----------
    
    x1 : array
      x axis of timeseries1 - plotted as a line
    y1 : array
     values of timeseries1 - plotted as a line
    x2 : array
        x axis of scatter points
    y2 : array
        y of scatter points
    figsize : list
        a list of two integers indicating the figure size
    xlabel : str
        label for x-axis
    ylabel : str
        label for y-axis
    title : str
        the title for the figure
    xlim : list
        set the limits of the x axis
    ylim : list
        set the limits of the y axis
    ax : pyplot.axis
        the pyplot.axis object
    legend : bool
        plot legend or not
    lgd_kwargs : dict
        the keyword arguments for ax.legend()
    plot_kwargs : dict
        the keyword arguments for ax.plot()
    savefig_settings : dict
        the dictionary of arguments for plt.savefig(); some notes below:
        - "path" must be specified; it can be any existed or non-existed path,
          with or without a suffix; if the suffix is not given in "path", it will follow "format"
        - "format" can be one of {"pdf", "eps", "png", "ps"}

    Returns
    -------
    
    ax : the pyplot.axis object
    
    See also
    -------- 
    
    pyleoclim.utils.plotting.set_style : set different styles for the figures. Should be set before invoking the plotting functions
    pyleoclim.utils.plotting.savefig : save figures
    
    '''
    # handle dict defaults
    savefig_settings = {} if savefig_settings is None else savefig_settings.copy()
    plot_kwargs = {} if plot_kwargs is None else plot_kwargs.copy()
    lgd_kwargs = {} if lgd_kwargs is None else lgd_kwargs.copy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    ax.plot(x1, y1, **plot_kwargs, color='green')
    ax.scatter(x2, y2, color='red')

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if title is not None:
        ax.set_title(title)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    if legend:
        ax.legend(**lgd_kwargs)
    else:
        ax.legend().remove()

    if 'fig' in locals():
        if 'path' in savefig_settings:
            savefig(fig, settings=savefig_settings)
        return fig, ax
    else:
        return ax


def plot_xy(x, y, figsize=None, xlabel=None, ylabel=None, title=None, 
            xlim=None, ylim=None,savefig_settings=None, ax=None,
            legend=True, plot_kwargs=None, lgd_kwargs=None,
            invert_xaxis=False, invert_yaxis=False):
    ''' Plot a timeseries
    
    Parameters
    ----------
    x : array
        The time axis for the timeseries
    y : array
        The values of the timeseries
    figsize : list
        a list of two integers indicating the figure size
    xlabel : str
        label for x-axis
    ylabel : str
        label for y-axis
    title : str
        the title for the figure
    xlim : list
        set the limits of the x axis
    ylim : list
        set the limits of the y axis
    ax : pyplot.axis
        the pyplot.axis object
    legend : bool
        plot legend or not
    lgd_kwargs : dict
        the keyword arguments for ax.legend()
    plot_kwargs : dict
        the keyword arguments for ax.plot()
    mute : bool
        if True, the plot will not show;
        recommend to turn on when more modifications are going to be made on ax
         (going to be deprecated)
    savefig_settings : dict
        the dictionary of arguments for plt.savefig(); some notes below:
        - "path" must be specified; it can be any existed or non-existed path,
          with or without a suffix; if the suffix is not given in "path", it will follow "format"
        - "format" can be one of {"pdf", "eps", "png", "ps"}
    invert_xaxis : bool, optional
        if True, the x-axis of the plot will be inverted
    invert_yaxis : bool, optional
        if True, the y-axis of the plot will be inverted
        
    Returns
    -------

    ax : the pyplot.axis object

    See Also
    --------
    
    pyleoclim.utils.plotting.set_style : set different styles for the figures. Should be set before invoking the plotting functions
    pyleoclim.utils.plotting.savefig : save figures        
    '''
    # handle dict defaults
    savefig_settings = {} if savefig_settings is None else savefig_settings.copy()
    plot_kwargs = {} if plot_kwargs is None else plot_kwargs.copy()
    lgd_kwargs = {} if lgd_kwargs is None else lgd_kwargs.copy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    ax.plot(x, y, **plot_kwargs)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if title is not None:
        ax.set_title(title)
        # TODO replace with ax.set_title(title, fontweight='bold') when all relevant plots use plot_xy

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    if legend:
        ax.legend(**lgd_kwargs)
    else:
        ax.legend().remove()

    if invert_xaxis:
        ax.invert_xaxis()
        
    if invert_yaxis:
        ax.invert_yaxis()

    if 'fig' in locals():
        if 'path' in savefig_settings:
            savefig(fig, settings=savefig_settings)
        return fig, ax
    else:
        return ax


def closefig(fig=None):
    '''Close the figure

    Parameters
    ----------
    fig : matplotlib.pyplot.figure
        The matplotlib figure object

    '''
    if fig is not None:
        plt.close(fig)
    else:
        plt.close()

def savefig(fig, path=None, dpi=300, settings={}, verbose=True):
    ''' Save a figure to a path

    Parameters
    ----------
    fig : matplotlib.pyplot.figure
        the figure to save
    path : str
        the path to save the figure, can be ignored and specify in "settings" instead
    dpi : int
        resolution in dot (pixels) per inch. Default: 300. 
    settings : dict
        the dictionary of arguments for plt.savefig(); some notes below:
        - "path" must be specified in settings if not assigned with the keyword argument;
          it can be any existed or non-existed path, with or without a suffix;
          if the suffix is not given in "path", it will follow "format"
        - "format" can be one of {"pdf", "eps", "png", "ps"}
    verbose : bool, {True,False}
        If True, print the path of the saved file.
        
    '''
    if path is None and 'path' not in settings:
        raise ValueError('"path" must be specified, either with the keyword argument or be specified in `settings`!')

    savefig_args = {'bbox_inches': 'tight', 'path': path, 'dpi': dpi}
    savefig_args.update(settings)

    path = pathlib.Path(savefig_args['path'])
    savefig_args.pop('path')

    dirpath = path.parent
    if not dirpath.exists():
        dirpath.mkdir(parents=True, exist_ok=True)
        if verbose:
            print(f'Directory created at: "{dirpath}"')

    path_str = str(path)
    if path.suffix not in ['.eps', '.pdf', '.png', '.ps']:
        path = pathlib.Path(f'{path_str}.pdf')

    fig.savefig(path_str, **savefig_args)
    plt.close(fig)

    if verbose:
        print(f'Figure saved at: "{str(path)}"')


def set_style(style='journal', font_scale=1.0, dpi=300):
    ''' Modify the visualization style
    
    This function is inspired by [Seaborn](https://github.com/mwaskom/seaborn).
   
    
    Parameters
    ----------
    
    style : {journal,web,matplotlib,_spines, _nospines,_grid,_nogrid}
        set the styles for the figure:
            - journal (default): fonts appropriate for paper
            - web: web-like font (e.g. ggplot)
            - matplotlib: the original matplotlib style
            In addition, the following options are available:
            - _spines/_nospines: allow to show/hide spines
            - _grid/_nogrid: allow to show gridlines (default: _grid)
    
    font_scale : float
        Default is 1. Corresponding to 12 Font Size. 
    
    '''
    font_dict = {
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
    }

    style_dict = {}
    if 'journal' in style:
        style_dict.update({
            'axes.axisbelow': True,
            'axes.facecolor': 'white',
            'axes.edgecolor': 'black',
            'axes.grid': True,
            'grid.color': 'lightgrey',
            'grid.linestyle': '--',
            'xtick.direction': 'out',
            'ytick.direction': 'out',
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif'],

            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.spines.right': False,
            'axes.spines.top': False,

            'legend.frameon': False,

            'axes.linewidth': 1,
            'grid.linewidth': 1,
            'lines.linewidth': 2,
            'lines.markersize': 6,
            'patch.linewidth': 1,

            'xtick.major.width': 1.25,
            'ytick.major.width': 1.25,
            'xtick.minor.width': 0,
            'ytick.minor.width': 0,
        })
    elif 'web' in style:
        style_dict.update({
            'figure.facecolor': 'white',

            'axes.axisbelow': True,
            'axes.facecolor': 'whitesmoke',
            'axes.edgecolor': 'lightgrey',
            'axes.grid': True,
            'grid.color': 'white',
            'grid.linestyle': '-',
            'xtick.direction': 'out',
            'ytick.direction': 'out',

            'text.color': 'grey',
            'axes.labelcolor': 'grey',
            'xtick.color': 'grey',
            'ytick.color': 'grey',

            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif'],

            'axes.spines.left': False,
            'axes.spines.bottom': False,
            'axes.spines.right': False,
            'axes.spines.top': False,

            'legend.frameon': False,

            'axes.linewidth': 1,
            'grid.linewidth': 1,
            'lines.linewidth': 2,
            'lines.markersize': 6,
            'patch.linewidth': 1,

            'xtick.major.width': 1.25,
            'ytick.major.width': 1.25,
            'xtick.minor.width': 0,
            'ytick.minor.width': 0,
        })
    else:
        raise ValueError(f'Style [{style}] not availabel!')

    if '_spines' in style:
        style_dict.update({
            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.spines.right': True,
            'axes.spines.top': True,
        })
    elif '_nospines' in style:
        style_dict.update({
            'axes.spines.left': False,
            'axes.spines.bottom': False,
            'axes.spines.right': False,
            'axes.spines.top': False,
        })

    if '_grid' in style:
        style_dict.update({
            'axes.grid': True,
        })
    elif '_nogrid' in style:
        style_dict.update({
            'axes.grid': False,
        })

    figure_dict = {
        'savefig.dpi': dpi,
    }

    # modify font size based on font scale
    font_dict.update({k: v * font_scale for k, v in font_dict.items()})

    for d in [style_dict, font_dict, figure_dict]:
        mpl.rcParams.update(d)










