import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import sys
import plot

from py_pol.stokes import Stokes, degrees


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

    plot.xyplot_from_csv(
        file="sweep.csv",
        x_index=0,
        y_indices=[2, 4],
        title=None,
        title_size=25,
        xlabel="Wavelength (nm)",
        ylabel="Power (dBm)",
        axis_label_size=18,
    )

    # plot.poincare_from_csv("pol_test.csv")

    plt.show()
