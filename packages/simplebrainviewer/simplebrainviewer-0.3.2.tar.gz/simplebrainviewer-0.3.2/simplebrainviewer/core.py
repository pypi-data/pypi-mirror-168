#!/usr/bin/env python3
"""
    A simple brain viewing tool with matplotlib

    Just something simple to quickly load and view 3D volumes with python
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import nibabel as nib
import numpy as np
from typing import Union

# set matplotlib global settings
mpl.rcParams["toolbar"] = "None"
mpl.rcParams["text.color"] = "#DDDDDD"

"""
    Define methods for control elements
"""


class Control:
    def __init__(self, figure, position, label, initial_value, dim):
        """
        Control group for slice
        """
        # Slider
        self.slider = Slider(
            figure.add_axes(position, xticks=[], yticks=[], facecolor="#222222"),
            label,
            0,
            dim - 1,
            valinit=initial_value,
            valstep=1,
            valfmt="%1.0f",
            color="#444444",
        )

        # Set Button Positions
        position[1] = position[1] - 0.04
        position[2] = position[2] / 2
        position[3] = 0.04
        self.buttondown = Button(figure.add_axes(position), "-", color="#222222", hovercolor="#333333")

        # Buttons
        position[0] = position[0] + position[2]
        self.buttonup = Button(figure.add_axes(position), "+", color="#222222", hovercolor="#333333")

        # save value for display
        self.value = initial_value

        # save dim for slider limit
        self.lim = dim

    def get_value(self):
        """
        Returns the current value of the control
        """
        return int(self.value)

    # decrement slider
    def decrement(self, event):
        new_val = self.value - 1
        if new_val >= 0:
            self.slider.set_val(new_val)

    # increment slider
    def increment(self, event):
        new_val = self.value + 1
        if new_val < self.lim:
            self.slider.set_val(new_val)

    # update control
    def update(self, value, callback_func):
        """
        Updates the current value of the control then runs the
        callback_func with the current value
        """
        self.value = int(value)  # set new value
        callback_func(int(value))  # execute callback


class ControlManager:
    def __init__(self, ax_dict, control_dict):
        self.ax_dict = ax_dict
        self.control_dict = control_dict

    def link(self, key, callback_func):
        # Link slider object
        # This call the update method on the control so that its current value is updated
        # before passing it to the display via the callback_func
        self.get_control(key).slider.on_changed(lambda x: self.get_control(key).update(x, callback_func))
        # Link increment/decrement buttons
        self.get_control(key).buttondown.on_clicked(self.get_control(key).decrement)
        self.get_control(key).buttonup.on_clicked(self.get_control(key).increment)

    def update(self, display, key, data, lims):
        # update the display
        display.set_data(data)
        plt.draw()

    def get_control(self, key):
        return self.control_dict[key]

    def get_ax(self, key):
        return self.ax_dict[key]


"""
    Brain viewer
"""


class BrainViewer:
    def __init__(self, img: Union[nib.Nifti1Image, np.ndarray], width=12, height=6):
        # Create figure and axes
        self.f = plt.figure(figsize=(width, height))
        self.f.canvas.manager.set_window_title("SimpleBrainViewer")
        self.f.patch.set_facecolor("#000000")
        ax0 = self.f.add_axes([0.06, 0.20, 0.28, 0.75])
        ax0.axis("off")
        ax1 = self.f.add_axes([0.36, 0.20, 0.28, 0.75])
        ax1.axis("off")
        ax2 = self.f.add_axes([0.66, 0.20, 0.28, 0.75])
        ax2.axis("off")
        plt.subplots_adjust(bottom=0.25)

        # get copy of data
        if type(img) is np.ndarray:
            data = img
        elif type(img) is nib.Nifti1Image:
            data = img.get_fdata()
        else:
            raise TypeError("Not a numpy array or Nifti1Image!")

        # set initial slices
        dim = data.shape
        if len(dim) == 3:  # if only 3 dims, add 4th
            data = data[:, :, :, np.newaxis]
            data = np.concatenate((data, data), axis=3)
            dim = data.shape
        Sinit = int(dim[0] / 2)
        Cinit = int(dim[1] / 2)
        Tinit = int(dim[2] / 2)
        Finit = 0

        # get data max/min
        dmax = data.max()
        dmin = data.min()

        # Create controls
        self.control_manager = ControlManager(
            {"sagittal": ax0, "coronal": ax1, "transverse": ax2},
            {
                "sagittal_control": Control(self.f, [0.1, 0.175, 0.2, 0.03], "S", Sinit, dim[0]),
                "coronal_control": Control(self.f, [0.4, 0.175, 0.2, 0.03], "C", Cinit, dim[1]),
                "transverse_control": Control(self.f, [0.7, 0.175, 0.2, 0.03], "T", Tinit, dim[2]),
                "frame_control": Control(self.f, [0.35, 0.075, 0.3, 0.03], "Frame", Finit, dim[3]),
            },
        )

        # define slice functions
        sagittal_slice = lambda x, t: data[x, :, :, t].T
        coronal_slice = lambda x, t: data[:, x, :, t].T
        transverse_slice = lambda x, t: data[:, :, x, t].T

        # create initial display
        d0 = self.control_manager.get_ax("sagittal").imshow(
            sagittal_slice(Sinit, Finit), origin="lower", cmap="gray", vmin=dmin, vmax=dmax
        )
        d1 = self.control_manager.get_ax("coronal").imshow(
            coronal_slice(Cinit, Finit), origin="lower", cmap="gray", vmin=dmin, vmax=dmax
        )
        d2 = self.control_manager.get_ax("transverse").imshow(
            transverse_slice(Tinit, Finit), origin="lower", cmap="gray", vmin=dmin, vmax=dmax
        )

        # add event listeners for each slice control
        # TODO: changed the display logic so need to redo some of the update method inputs
        self.control_manager.link(
            "sagittal_control",
            lambda x: self.control_manager.update(
                d0,
                "sagittal",
                sagittal_slice(
                    int(x), self.control_manager.get_control("frame_control").get_value()
                ),  # callback to execute
                [dmin, dmax],
            ),
        )
        self.control_manager.link(
            "coronal_control",
            lambda x: self.control_manager.update(
                d1,
                "coronal",
                coronal_slice(
                    int(x), self.control_manager.get_control("frame_control").get_value()
                ),  # callback to execute
                [dmin, dmax],
            ),
        )
        self.control_manager.link(
            "transverse_control",
            lambda x: self.control_manager.update(
                d2,
                "transverse",
                transverse_slice(int(x), self.control_manager.get_control("frame_control").get_value()),
                [dmin, dmax],
            ),
        )

        # simply update all other controls with the frame control
        def framefunc(frame):
            # just set each of the sliders to their current values, but it should parse the updated
            # frame info (We don't need to use the frame value because it should auto grab it)
            self.control_manager.get_control("sagittal_control").slider.set_val(
                self.control_manager.get_control("sagittal_control").get_value()
            )
            self.control_manager.get_control("coronal_control").slider.set_val(
                self.control_manager.get_control("coronal_control").get_value()
            )
            self.control_manager.get_control("transverse_control").slider.set_val(
                self.control_manager.get_control("transverse_control").get_value()
            )

        self.control_manager.link("frame_control", framefunc)


"""
    Create BrainViewer object and plot the figure
"""


def plot_brain(data, block=True):
    brainviewer = BrainViewer(data)
    plt.show(block=block)
    # if you are non-blocking, assign the return value
    # to something to keep the plot reference alive
    return brainviewer
