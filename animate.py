try: import numpy as np
except: raise ModuleNotFoundError("You need numpy to use this module. Please install it via pip install numpy.")
try: import matplotlib.pyplot as plt
except: raise ModuleNotFoundError("You need matplotplib to use this module. Please install it via pip install matplotlib.")
try: import matplotlib.animation as animation
except: raise ModuleNotFoundError("Failed to load the animation module.")
from typing import Callable, Union

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
        self.max_plots = max_plots
        self.range = np.linspace(0, 5, 100)
        self.lines = []
        self.fig, self.ax = plt.subplots()
        self.attrs = {k: dict() for k in range(max_plots)}
    
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
    
    def set_func(self, func: Callable):
        """
        Set a function to be plotted.

        Parameters
        ----------
        `func` : `Callable` - Function.

        Return
        -------
        `self` : The `Animate` object.
        """
        if len(self.funcs) < self.max_plots:
            self.funcs.append(func)
        else:
            raise ValueError("You have reached the maximum number of functions allowed. Please change the max_plots attribute to add more!")
        return self
    
    def set_xrange(self, amin: float, amax: float, frames: int, *, padding: Union[float, tuple[float]] = 0):
        """
        Set the range of the x-axis.

        Parameters
        ----------
        `amin` : `float` - Lower bound of axis range.
        `amax` : `float` - Upper bound of axis range.
        `frames` : `int` - Total number of frames. The more frames, the slower the animation.

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
        `padding` : `float` - Optional parameter to define the vertical padding.

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
        for idx, _ in enumerate(self.funcs):
            ln, = self.ax.plot([], [], **self.attrs[idx])
            self.lines.append(ln)

        return self.lines
    
    def __update(self, num: int):
        for line, func in zip(self.lines, self.funcs):
            x = self.range
            y = func(x)
            line.set_data(x[:num], y[:num])

        return self.lines

    def animate(self, interval: int = 20, repeat: bool = True, save: bool = False, *, chdir: str = None, _format: str = "mp4", fps: int = 30, dpi: int = 300, **kwargs):
        """
        Start the animation.

        Parameters
        ----------
        - `interval` : `int` - Determines how fast the animation is. The smaller the value, the faster.
        - `repeat` : `bool` - Whether to repeat the animation when it has ended.
        - `kwargs` : `dict[str, any]` - Pass additional arguments to the `FuncAnimation` class.
        """
        ani = animation.FuncAnimation(self.fig, self.__update, len(self.range), init_func=self.__init_axes, interval=interval, blit=True, cache_frame_data=False, repeat = repeat, **kwargs)
        if not save: plt.show()
        else: 
            if chdir: 
                import os 
                os.chdir(chdir)
            ani.save(f"Animation.{_format}", fps = fps, dpi = dpi)

# ani = Animate()
# cosine = lambda x : np.cos(x)
# sine = lambda x : np.sin(x)
# exp = lambda x : np.exp(-x)
# sine2 = lambda x : np.sin(x**2)
# ani.ax.spines[['right', 'top']].set_visible(False)
# ani.ax.set_title("Testing Animation Constructor", fontdict={'weight' : 'bold', 'size' : 16})
# ani.set_funcs([cosine, sine, sine2, exp]).set_xrange(0, 10, 500).set_yrange(-3, 2).set_plot_attrs(1, color='purple').set_plot_attrs(0, color = 'green').animate(interval=5, save = False)