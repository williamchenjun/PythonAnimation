try: import numpy as np
except: raise ModuleNotFoundError("You need numpy to use this module. Please install it via pip install numpy.")
try: import matplotlib.pyplot as plt
except: raise ModuleNotFoundError("You need matplotplib to use this module. Please install it via pip install matplotlib.")
try: import matplotlib.animation as animation
except: raise ModuleNotFoundError("Failed to load the animation module.")
from typing import Callable, Union
from Lines import Lines
from time import sleep
from datetime import datetime, timedelta
from multiprocessing import Process

class Animate:
    """
    Create animated plots using `matplotlib.pyplot` easily with the `Animate` constructor!

    Parameters
    ----------
    - `max_plots`:`int` - Optional parameter to increase the maximum number of allowed plots. Note that increasing the threshold may reduce the perfomance of your machine.

    Methods
    -------
    - `set_funcs` : Allows you to set a list of functions to plot. They should be single variable functions passed as a callable.
    - `set_func` : Allows you to set a singular function.
    - `set_xrange` : Allows you to set the range of the x-axis for both the plot and function.
    - `set_yrange` : Allows you to set the range of the y-axis.
    - `set_plot_attrs` : Allows you to set attributes for the plots. You can target each plot by indexing them.
    - `set_axes_attrs` : Allows you to set attributes for the axes.
    - `animate` : Starts the animation.
    """
    def __init__(self, *, max_plots: int = 10) -> None:
        self.funcs = []
        self.inv_idxs = []
        self.sleep_idxs = dict()
        self.max_plots = max_plots
        self.range = np.linspace(0, 5, 100)
        self.lines = []
        self.fig, self.ax = plt.subplots()
        self.attrs = {k: dict() for k in range(max_plots)}
        self.acc_delay = {k: 0 for k in range(max_plots)}
        self.animation_started = True
        self.current_time = dict()
    
    def set_funcs(self, funcs: list[Callable]):
        """
        Set a list of functions to be plotted.

        Parameters
        ----------
        `funcs` : `list[Callable]` - List of functions.

        Return
        -------
        `self` : The `Animate` object.
        """
        if len(self.funcs) + len(funcs) < self.max_plots:
            for func in funcs:
                self.funcs.append(func)
        else:
            raise ValueError("You have reached the maximum number of functions allowed. Please change the max_plots attribute to add more!")
        return self
    
    def set_func(self, func: Callable, inverse: bool = False, _sleep: int = None):
        """
        Set a function to be plotted.

        Parameters
        ----------
        `func` : `Callable` - Function.
        `inverse` : `bool` - Whether you want to plot the function inverting the x and y values.
        `_sleep` : `int` - Delay the start of an animation (in seconds).

        Return
        -------
        `self` : The `Animate` object.
        """
        if len(self.funcs) < self.max_plots:
            if _sleep: self.sleep_idxs[len(self.funcs)] = _sleep
            if inverse: self.inv_idxs.append(len(self.funcs))
            self.funcs.append(func)
        else:
            raise ValueError("You have reached the maximum number of functions allowed. Please change the max_plots attribute to add more!")
        return self

    def animate_point(self):
        ...
    
    def set_xrange(self, amin: float, amax: float, frames: int, *, padding: Union[float, tuple[float]] = 0):
        """
        Set the range of the x-axis.

        Parameters
        ----------
        `amin` : `float` - Lower bound of axis range.
        `amax` : `float` - Upper bound of axis range.
        `frames` : `int` - Total number of frames. The more frames, the slower the animation.
        `padding` : `float` or `tuple` - Optional parameter to define the horizontal padding. If a tuple is passed, the first value represents the left padding and the second one the right padding.

        Return
        -------
        `self` : The `Animate` object.
        """
        
        self.range = np.linspace(amin, amax, frames)
        if type(padding) in (float, int): self.ax.set_xlim(amin - padding, amax + padding)
        elif type(padding) in (list, tuple) and len(padding) == 2: self.ax.set_xlim(amin - padding[0], amax + padding[1])
        else: raise TypeError("The padding should either be a number or an iterable of length 2.")
        return self
    
    def set_yrange(self, amin: float, amax: float, *, padding: Union[float, tuple[float]] = 0):
        """
        Set the range of the y-axis.

        Parameters
        ----------
        `amin` : `float` - Lower bound of axis range.
        `amax` : `float` - Upper bound of axis range.
        `padding` : `float` or `tuple` - Optional parameter to define the vertical padding. If a tuple is passed, the first value represents the lower padding and the second one the upper padding.

        Return
        -------
        `self` : The `Animate` object.
        """

        if type(padding) in (float, int): self.ax.set_ylim(amin - padding, amax + padding)
        elif type(padding) in (list, tuple) and len(padding) == 2: self.ax.set_ylim(amin - padding[0], amax + padding[1])
        else: raise TypeError("The padding should either be a number or an iterable of length 2.")
        return self
    
    def set_plot_attrs(self, idx: int, **plot_kwargs):
        """
        Set the attributes of the desired plot.

        Parameters
        ----------
        `idx` : `int` - Target plot index.
        `plot_kwargs` : `dict[str, any]` - Attributes. Pass them as keyword and value, e.g. `color = 'red'`.

        Return
        -------
        `self` : The `Animate` object.
        """
        for key, val in plot_kwargs.items():
            self.attrs[idx][key] = val
        
        return self

    def set_axes_attrs(self, **ax_kwargs):
        """
        Set the attributes of the axis.

        Parameters
        ----------
        `ax_kwargs` : `dict[str, any]` - Attributes. Pass them as keyword and value, e.g. `title = 'Plot'`.

        Return
        -------
        `self` : The `Animate` object.
        """
        self.ax.set(**ax_kwargs)
        return self
    
    def __init_axes(self):
        x = self.range
        for idx in range(len(self.funcs)):
            ln, = self.ax.plot([], [], **self.attrs[idx])
            self.lines.append(ln)

        return self.lines
    
    def __update(self, num: int):
        for idx, (line, func) in enumerate(zip(self.lines, self.funcs)):
            
            if idx in self.sleep_idxs.keys():
                if self.animation_started:
                    self.current_time[idx] = datetime.now()
                curr_time = datetime.now()
                if (curr_time - self.current_time[idx]).total_seconds() < self.sleep_idxs[idx]:
                    self.acc_delay[idx] += 1
                    continue
                else:
                    pass

            x = self.range
            y = func(x)
            
            if idx in self.inv_idxs:
                if idx not in self.sleep_idxs.keys(): 
                    if num <= len(self.range): line.set_data(y[:num], x[:num])
                else:
                    if (num - self.acc_delay[idx]) >= 0: line.set_data(y[:(num - self.acc_delay[idx])], x[:(num - self.acc_delay[idx])])
            else:
                if idx not in self.sleep_idxs.keys(): 
                    if num <= len(self.range): line.set_data(x[:num], y[:num])
                else:
                    if (num - self.acc_delay[idx]) >= 0: line.set_data(x[:(num - self.acc_delay[idx])], y[:(num - self.acc_delay[idx])])
                
        self.animation_started = False
        return self.lines

    def animate(self, interval: int = 20, repeat: bool = True, save: bool = False, *, chdir: str = None, _format: str = "mp4", fps: int = 30, dpi: int = 300, duration: int = None, **kwargs):
        """
        Start the animation.

        Parameters
        ----------
        - `interval` : `int` - Determines how fast the animation is. The smaller the value, the faster.
        - `repeat` : `bool` - Whether to repeat the animation when it has ended.
        - `save` : `bool` - Save animation on the current directory.
        - `chdir` . `str` - Change directory.
        - `_format`: `str` - Animation format.
        - `fps`: `int` - Frames per second (valid only for saved video).
        - `dpi`: `int` - Dots per inch. The higher the number, the better the quality (valid only for saved video).
        - `duration` : `int` - Define how long you want the video to be. Note that this will override custom `interval` and `fps`.
        - `kwargs` : `dict[str, any]` - Pass additional arguments to the `FuncAnimation` class.
        """
        if len(self.sleep_idxs): frames = len(self.range) + int((max(self.sleep_idxs.values()) + 1)*1000/interval)
        else: frames = len(self.range)

        if not save: 
            if duration:
                interval = int(1000*duration/frames)
            ani = animation.FuncAnimation(self.fig, self.__update, frames, init_func=self.__init_axes, interval=interval, blit=True, cache_frame_data=False, repeat = repeat, **kwargs)
            plt.show()

        else: 
            if len(self.sleep_idxs) and not repeat: raise ValueError("You cannot define delays and have repeat set to False. This would generate an incomplete graph.")
            if duration:
                fps = int(frames / duration)

            if chdir: 
                import os 
                os.chdir(chdir)
            ani = animation.FuncAnimation(self.fig, self.__update, frames, init_func=self.__init_axes, interval=interval, blit=True, cache_frame_data=False, repeat = repeat, **kwargs)
            ani.save(f"Animation.{_format}", fps = fps, dpi = dpi)