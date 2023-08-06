from scipy import stats
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import matplotlib.mlab as mlab
import plotly
import plotly.tools as tls
from tkinter import *
import os


def plotly_reg(x, y, fig, rc, clr, description_txt='', x_var_name ='', y_var_name ='',
               xaxis = None, yaxis = None, xlbl ='', ylbl ='',
               scatter_plot = 0, range=None, ax_mpl=None, mpl_clr=None):
    '''Doing regression plot using plotly
    rc = regression comtour'''
    # Calculating the regression line
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[~np.isnan(y)], y[~np.isnan(y)])
    y_reg = slope * x + intercept
    reg_analysis = 'r = %.2f p = %.2f' % (r_value, p_value)
    reg_equation = y_var_name + ' = %.2f*' % (slope)
    reg_equation += x_var_name + '%+.2f' % (intercept)
    temp_text = description_txt + ', ' + reg_analysis + ', ' + reg_equation

    # Plotting the regression line
    line = go.Scatter(x=x, y=y_reg, mode='lines+text', line=dict(width=2, color=clr),
                      name=temp_text)
    fig.append_trace(line, rc[0], rc[1])

    # Plotting scatter of the data
    if scatter_plot == 1:
        trace = go.Scatter(x=x, y=y, mode='markers', marker=dict(color='rgb'))
        fig.append_trace(trace, rc[0], rc[1])

    if yaxis != None and xaxis != None:
        fig['layout'][yaxis].update(title=ylbl)
        fig['layout'][xaxis].update(title=xlbl)

    if ax_mpl != None:
        ax_mpl.plot(x, y_reg, label=description_txt, color=mpl_clr)

    return slope, intercept, r_value, p_value, std_err


def format_axis(ax, xlbl, ylbl, ind = None):
    '''
    format axis of matplotlib
    example: format_axis(ax[0], ylbl='Entanglement', xlbl='Questions order')
    :param ind:
    :return:
    '''
    ax.set_ylabel(ylbl)
    ax.set_xlabel(xlbl)
    ax.legend()

    if ind != None:
        ax.set_xticks(ind)
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.set_xticklabels(ind)
        for label in ax.get_xmajorticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment("right")


def show_message(file_name):
    '''Prints text message from txt file'''
    fl1 = open(file_name, 'r')
    f_str = fl1.read()
    fl1.close()
    # Output a message
    root = Tk()
    w = Label(root, text=f_str)
    w.pack()
    root.mainloop()


def save_maxfig(fig, fig_name, save_plotly=False, transperent = False, frmt='png', resize=None):
    '''
    Save figure in high resolution
    example:
    save_maxfig(fig,fig_name, save_plotly=True, transperent=True, frmt='eps', resize=[18,6])
    :param fig: figure
    :param fig_name: file name
    :param save_plotly: save to plotly also
    :param transperent: no background
    :param frmt: file format
    :param resize: size
    :return:
    '''
    # matplotlib.rcParams.update({'font.size': 40})
    fig.set_size_inches(12, 12)
    if resize != None:
        fig.set_size_inches(resize[0], resize[1])
    fig_name+='.'+frmt
    plt.savefig(fig_name, dpi=300, format=frmt)

    if save_plotly :
        # offline plotting
        plotly_fig = tls.mpl_to_plotly(fig)
        plotly_fig_name = + fig_name + '.html'
        plotly_fig['layout'].update(height=1500, width=800, showlegend=False)
        plotly.offline.plot(plotly_fig, filename=plotly_fig_name, auto_open=False)  # offline ploty


def manual_matplotlib_crop(fullImage):
    '''
    Manually crop part of the image.
    @param fullImage: Image to crop
    @return: the cropped image.
    '''

    def line_select_callback(eclick, erelease):
        '''
        Get x1, y1 when cliked and x2,y2 when released.
        '''
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

    def toggle_selector(event):
        '''
        (de) Activate the selector.
        '''
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)



    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.imshow(fullImage)

    toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1,3],
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=True)

    plt.connect('key_pressed_event', toggle_selector)
    plt.show()
    cropCoords = [int(x) for x in toggle_selector.RS.extents]

    croopedIm = fullImage[cropCoords[2]:cropCoords[3], cropCoords[0]:cropCoords[1]]

    return croopedIm


# if __name__ == '__main__':
#
#     im = plt.imread('car.png')
#     cIm = manual_matplotlib_crop(im)
#     plt.imshow(cIm)
#     plt.show()
