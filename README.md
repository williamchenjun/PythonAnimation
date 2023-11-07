# Introduction

> Note: This is not the final version.

If you're looking to animating your plots in Python, you could benefit from using this module. It is a simple class called `Animate` and it is just as simple as defining the function you want to plot and it is done! It's still just a prototype, but I will be updating this in order to animate more types of plots.

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
anim.set_func(f).set_xrange(0, 10, 500).set_yrange(-1, 1, padding = 1).set_plot_attrs(0, color = 'orange', lw = 3).animate(save=True, fps = 60)
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
anim.animate(save=True, fps = 60)
```

You can obviously decide to call each method separately instead of concatenating everything, which might become less readable. As you can see we just use `set_funcs` instead of `set_func`, and we can target each function (in order) to set their own attributes:
<video src="https://github.com/williamchenjun/PythonAnimation/assets/79821802/9a702ca5-616b-43a5-b6aa-78b6f512f6b4"></video>



