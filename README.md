# Introduction

> Note: This is not the final version.

If you're here because you want to animate your plots in Python, you could benefit from using this module. It is a simple class called `Animate` and it is just as simple as defining the function you want to plot and it is done! It's still just a prototype, but I will be updating this in order to animate more types of plots.

# How to install

You can start using this either by manually making a copy of the code, or you can clone this repo in your work directory:
```shell
git clone https://github.com/williamchenjun/PythonAnimation.git
```

# How to use

The first thing to do is to import the class from `animate.py`

```python
from animate import Animate
```

## Simple animation example

Let's assume that we want to plot and animate $$f(x) = \sin(x \cdot \sin(x)).$$

then it is as simple as the running the following code

```python
from animate import Animate
import numpy as np

def f(x):
  return np.sin(x*np.sin(x))

anim = Animate()
anim.set_func(f).set_xrange(0, 10, 200).set_yrange(-1, 1).animate()
```

which will generate the following
<video src='https://github.com/williamchenjun/PythonAnimation/assets/79821802/353919a1-d238-4cbf-aaff-0351263c3247'></video>

> The video was saved by passing the `save = True` argument to `animate`. I have also increased the fps to 60.

### Simple customization

It is just as simple to customize your plots by using the `set_plot_attrs` method. For example, if we want to change the line color, make it thicker, perhaps remove the right and top axes, we can just run the following script

```python
from animate import Animate
import numpy as np

def f(x):
  return np.sin(x*np.sin(x))

anim = Animate()
anim.ax.spines[['right', 'top']].set_visible(False)
anim.set_func(f).set_xrange(0, 10, 500).set_yrange(-1, 1, padding = 1).set_plot_attrs(0, color = 'orange', lw = 3).animate()
```
as you can see it is very simple and you can also still access the `matplotlib` components themselves, such as the `Axes` and `Figure`.

<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/34871323-14cf-4aba-8b92-db25ea07d577"></video>

## Multiple plots example

Lastly, it is also very simple to plot multiple plots at the same time!

> Note: The plots will automatically be sharing the same x-axis. I will be working on making separate animated subplots.

Let's assume we want to plot $$f(x) = \cos(x), \hspace{1em} g(x) = \sin(x).$$ This can be done simply 

```python
from animate import Animate
import numpy as np

def f(x):
  return np.cos(x)

def g(x):
  return np.sin(x)

anim = Animate()
anim.ax.spines[['right', 'top']].set_visible(False)
anim.set_funcs([f, g]).set_xrange(0, 10, 500).set_yrange(-1, 1, padding = 1)
anim.set_plot_attrs(0, color = 'orange', lw = 3)
anim.set_plot_attrs(1, color = 'green', lw = 3, ls = 'dashed')
anim.animate()
```

You can obviously decide to call each method separately instead of concatenating everything, which might become less readable. As you can see we just use `set_funcs` instead of `set_func`, and we can target each function (in order) to set their own attributes:
<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/9a702ca5-616b-43a5-b6aa-78b6f512f6b4"></video>

## Animating vertical lines and inverses

You can also implement animations where functions "grow" upwards rather than left to right. For example, if we consider the function

```math
f(x) = x^2 \implies x = \sqrt{y}
```
we can animate this by specifying the `inverse` argument in `set_func`

```python
from animate import Animate
import numpy as np

def f(y):
  return y**2

anim = Animate()
anim.ax.spines[['right', 'top']].set_visible(False)
anim.set_func(f, inverse = True).set_xrange(-1, 5, 500).set_yrange(-2, 2, padding = 1)
anim.set_plot_attrs(0, color = 'violet', lw = 3)
anim.animate()
```

which generates the following

<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/533868ef-a3dc-4e4b-80c0-ccb6c626964b
"></video>

As we can see, we don't need to write the inverse function itself. If we define the inverse parameter, it will automatically invert it. If you write the inverse function, and set `inverse` to `True` then it will just output the original non-inverted function.

I have also included an additional module called `Lines.py` in this repository. It is just a utility class to define vertical and horizontal lines. We can use those in conjuction to the `inverse` property to animate vertical lines:

```python
from animate import Animate
from Lines import Lines
import numpy as np

def f(x):
  return x

def g(x):
  return x**2

def h(x):
  return np.sin(x)

anim = Animate()
line = Lines()
anim.ax.spines[['right', 'top']].set_visible(False)
anim.set_func(f).set_xrange(0, 5, 500).set_yrange(0, 5)
anim.set_func(line.vline(x = 2), inverse=True, _sleep = 1)
anim.set_func(line.vline(x = 4), inverse=True, _sleep = 2)
anim.set_func(line.hline(y = 2), _sleep = 1)
anim.set_plot_attrs(0, lw = 3, color = 'blueviolet')
anim.set_plot_attrs(1, lw = 3, ls = 'dashed', color = 'mediumturquoise')
anim.set_plot_attrs(2, lw = 3, ls = 'dashed', color = 'limegreen')
anim.set_plot_attrs(3, lw = 3, ls = 'dashed', color = 'lightsalmon')
anim.ax.set_title("Testing vertical and horizontal lines".title(), fontdict = {'weight' : 'bold', 'size' : 15, 'family' : 'Helvetica', 'color' : '#393939'})
anim.animate(save = True, duration = 5)
```
which outputs the following

<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/62bd9a78-4110-4c36-8553-56fdf744c18f"></video>

> Note: The code looks very messy, but you could easily define a few functions since they don't really require much changing.

## Delay Animation

> **Note**: This is still a work in progress.

If you want your plots to start at a different time, you can do this by specifying the `_sleep` parameter in the `set_func` method. This is still not available for the `set_funcs` method. 

It can be achieved easily in the following way:

```python
from animate import Animate
import numpy as np

def f(x):
  return x**3

def g(x):
  return x**2

def h(x):
  return np.sin(x)

anim = Animate()
anim.ax.spines[['right', 'top']].set_visible(False)
anim.set_func(f).set_xrange(-1.5, 1.5, 500).set_yrange(-3, 3, padding = 0.5)
anim.set_func(g, _sleep = 1)
anim.set_func(h, _sleep = 2)
anim.set_plot_attrs(0, color = 'indianred', lw = 3)
anim.set_plot_attrs(1, color = 'dodgerblue', lw = 3, ls = 'dotted')
anim.set_plot_attrs(2, color = 'mediumpurple', lw = 5, ls = 'dashdot')
anim.animate(duration=5, save=True)
```

which will result in the following animation

<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/e0d8762d-7ee3-4b46-be5b-9aaf62b3efc3
"></video>

> Note: You can specify the duration of the video output by passing the `duration` in seconds. The video will end when all animations terminate (once).

