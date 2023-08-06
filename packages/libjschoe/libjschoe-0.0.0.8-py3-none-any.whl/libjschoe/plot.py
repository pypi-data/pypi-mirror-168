import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import sys

from py_pol.stokes import Stokes, degrees


def contour_from_csv(
    file,
    title=None,
    title_size=25,
    x_label=None,
    x_index=2,
    y_label=None,
    y_index=3,
    z_label=None,
    z_index=4,
    resolution=50,
    contour_method="linear",
    levels=10,
    axis_label_size=18,
    style="lfc",
    tick_fontsize=16,
    colorbar_fontsize=16,
    colormap="viridis",
):
    """
    Generate contour plot from csv file.

    Args:
        file (str): csv file name for contour plot. Defaults to "result.csv".
        title (_type_, optional): Title of the plot. Defaults to None.
        x_label (str, optional): x-axis label. If not specified or set to None, the name of the column with index of x_index is used as the label.  Defaults to None.
        x_index (int, optional): The index of the column used as the x axis. 0 means the leftmost column. Defaults to 2.
        y_label (str, optional): y-axis label. If not specified or set to None, the name of the column with index of y_index is used as the label.  Defaults to None.
        y_index (int, optional): The index of the column used as the y axis. 0 means the leftmost column. Defaults to 3.
        z_label (_type_, optional): z-axis label. If not specified or set to None, the name of the column with index of z_index is used as the label.  Defaults to None.
        z_index (int, optional): The index of the column used as the z axis. 0 means the leftmost column. Defaults to 4.
        resolution (int, optional): _description_. Defaults to 50.
        contour_method (str, optional): Defaults to "linear".
        levels (int, optional): The number of levels. Defaults to 10.
        axis_label_size (int, optional): The font size of axis labels. Defaults to 18.
        style (str, optional): The style of the contour plot. 'l': line, 'f':filled, 'lf' or 'fl': line and filled. 'c': contour line label and only valid with 'l'. Defaults to "lfc".
        colormap (str, optional): The colormap of the plot. Defaults to 'viridis'.
    """
    if file == None:
        print("No file name specified.")
        sys.exit(-1)
    df = pd.read_csv(file)
    column_list = list(df.columns)

    x = df[column_list[x_index]].values
    y = df[column_list[y_index]].values
    z = df[column_list[z_index]].values

    X, Y, Z = _plot_contour(x, y, z, resolution, contour_method)

    with plt.style.context("seaborn-white"):
        fig, ax = plt.subplots(figsize=(13, 8))
        # ax.scatter(x, y, color="black", linewidth=1, edgecolor="ivory", s=50)
        # ctr = ax.contour(X, Y, Z, levels, cmap="Blues")
        if "f" in style:
            CS = ax.contourf(X, Y, Z, cmap=colormap, alpha=1, levels=levels)  # alpha=1)
            cbar = fig.colorbar(CS)

            if z_label is None:
                cbar.ax.set_ylabel(column_list[z_index], fontsize=axis_label_size)
            else:
                cbar.ax.set_ylabel(z_label, fontsize=18)
        else:
            pass

        if "l" in style:
            cl = plt.contour(X, Y, Z, levels=levels, linewidths=0.5, colors="k")
            if "c" in style:
                ax.clabel(cl, fmt="%2d", inline=False, fontsize=colorbar_fontsize)

        if title is not None:
            ax.set_title(title, fontsize=title_size)
        else:
            ax.set_title(file[:-4], fontsize=title_size)
            # plot title is the file name without the extension

        if x_label is None:
            ax.set_xlabel(column_list[x_index], fontsize=axis_label_size)
        else:
            ax.set_xlabel(x_label, fontsize=18)

        if y_label is None:
            ax.set_ylabel(column_list[y_index], fontsize=18)
        else:
            ax.set_ylabel(y_label, fontsize=axis_label_size)

        plt.xticks(fontsize=tick_fontsize)
        plt.yticks(fontsize=tick_fontsize)

        plt.show()


def _plot_contour(x, y, z, resolution=50, contour_method="linear"):
    resolution = str(resolution) + "j"
    X, Y = np.mgrid[
        min(x) : max(x) : complex(resolution), min(y) : max(y) : complex(resolution)
    ]
    points = [[a, b] for a, b in zip(x, y)]
    Z = griddata(points, z, (X, Y), method=contour_method)
    return X, Y, Z


def xyplot_from_csv(
    file,
    x_index=0,
    y_indices=[1],
    title=None,
    title_size=25,
    xlabel=None,
    ylabel=None,
    axis_label_size=18,
    tick_fontsize=16,
    colormap="viridis",
):
    if file == None:
        print("No file name specified.")
        sys.exit(-1)
    df = pd.read_csv(file)
    column_list = list(df.columns)

    colorlist = [
        "red",
        "blue",
        "green",
        "yellow",
        "black",
        "orange",
        "purple",
        "brown",
        "pink",
        "gray",
    ]
    markerlist = [
        "o",
        "^",
        "s",
        "*",
        "D",
        "v",
        "x",
        "d",
        "P",
        "X",
        "h",
        "H",
        "8",
        "p",
        "|",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
    ]
    y_num = len(y_indices)
    y = []
    x = df[column_list[x_index]].values
    for i in range(y_num):
        y.append(df[column_list[y_indices[i]]].values)
        plt.plot(
            x,
            y[i],
            color=colorlist[i],
            linewidth=1,
            marker=markerlist[i],
            markersize=5,
            label=column_list[y_indices[i]],
        )
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.legend()

    plt.show()


def poincare_from_csv(file, title="Measured Polarization States"):
    """
    Plot polarization states measured  in a Poincare plot.
    Supported data file is from Thorlab polarimeter.
    After call poincare(), plt.show() is needed to show the plot.

    Args:
        file (string): The file name of the data file to plot. csv file.
        title (str, optional): Plot title. Defaults to 'Measured Polarization States'.
    """

    az = []
    el = []
    dop = []

    header = pd.read_csv(file, index_col=0, header=7, nrows=0, sep=";").columns.tolist()

    col_list = header[0:11]

    measured_pts = pd.read_csv(file, header=7, sep=";", usecols=col_list)

    az.append(measured_pts[header[8]] * degrees)
    el.append(measured_pts[header[9]] * degrees)
    dop.append(measured_pts[header[10]] / 100)

    # print(az)

    total_az = pd.concat(az)
    total_el = pd.concat(el)
    total_dop = pd.concat(dop)

    # print(total_az)

    SS = Stokes(title)

    SS.general_azimuth_ellipticity(
        azimuth=total_az, ellipticity=total_el, degree_pol=total_dop,
    )

    ax, fig = SS.draw_poincare(axis_equal=True)

    ax[0].set_box_aspect((2, 2, 2))
    # plt.show()


if __name__ == "__main__":

    # contour_from_csv(
    #     file="res.csv",
    #     x_index=0,
    #     x_label="Voltage 1 (V)",
    #     y_index=3,
    #     y_label="Voltage 2 (V)",
    #     z_index=6,
    #     z_label="Measured Power (dBm)",
    #     levels=25,
    #     style="lcf",
    #     colormap="bwr",
    # )

    # xyplot_from_csv(
    #     file="res.csv",
    #     x_index=0,
    #     y_indices=[1, 4],
    #     title=None,
    #     title_size=25,
    #     x_label=None,
    #     y_label=None,
    #     axis_label_size=18,
    # )

    poincare_from_csv("pol_test.csv")
    plt.show()
