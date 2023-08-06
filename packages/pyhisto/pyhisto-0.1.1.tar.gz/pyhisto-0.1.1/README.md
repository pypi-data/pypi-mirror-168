# Python Histogram module

This librabry provides histogram classes to perform data analysis.

Contrary to some data analysis library such as `Pandas` which generate histogram on demand from the whoel set of data, this library **just stores** the histogram in bins. 

The histograms are exported as ascii files (and can be reloaded from these files).

## Getting Started 

The following instructions will get you a copy of the project up and running on your local machine.

### Installing

There are several ways to install the module:

- :thumbsup: (recommended): use `pip`. The pyhisto is uploaded to the PyPi repository, so just running `pip install pyhisto` should install the library on your local environnement. 
- Download the [`pyhist.tar.gz`](dist/pyhisto-dev202005.tar.gz) file, unzip and run the `setup` script withing the directory:`$  python3 setup.py install`
- Get a local copy of the git directory (not recommenced)

### Dependencies

`pyhisto` is build with no dependencies for the use of histograms. For more advanced features in the `pyhist.tools` submodule, you will need `numpy` and `matplotlib` installed. If they are not, the features using them won't work, but the rest of the library will still load and be useable.

# Usage

The `pyhisto` module can be tested live (in cunjunction with another library) on Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.in2p3.fr%2Fgregoire.henning%2Ffaster-example-notebook/bb2c4cd04cf46352e7de83f88c11d91832f4cd60?filepath=example_notebook.ipynb)

## Bin

The basic for 1D histograms is a `Bin` object. That is an object that keep record of the number of counts between to values (edges). 

Main properties are:
- `Bin.count`
- `Bin.lowedge`
- `Bin.upedge`

Main methods are:
- `Bin.width()`
- `Bin.center()`


The bin can be typed into a `str` or `float`. Using `Bin(fromstring=z)`, the Bin is instanciated using the `z` string, as formated by `str(Bin)`.
`Bin` objects can be added together, or mutliplied and divied by floats. Comparison operators (`<`, `>`, ...) on a `Bin` are comparing `Bin.count`.


## Histogram

The basis class is `Histogram` which is `Bin` container with added function for management. 

`Histogram` is instantiated several ways: 
- `Histogram(nbins: int, xmin: float = -0.5, xmax: Optional)`: where `nbins` is the number of bins, `xmin` the low edge of the first bin, and `xmax` the up edge of the last bin. If `xmin` is not given, it is set at `-0.5` (so that it's centered on 0). If `xmax` is not given it is taken as `xmin + nbins`.
- `Histogram(fromstring: str)` where the argument is a string, formatted as `str(Histogram)` return.
- `Histogram(fromfile: :str)` where the argument is a file path where to read a string (just like `fromstring`).
- `Histogram(frombins: list)` with a list of `Bin` object.

When used as a container/list (i.e. `Histogram[i]`, `for in` loops, ...) `Histogram` behaves like a list of the bins. `+`, `-`, `*`, `\` operators either operates between one histogram and a scalar, or between two histograms of the same number of bins (no checking of bins limits is done).

-empty

index, find, fastindex, slice 
fill, fast fill

-copye, empty copy

xy

autocrop, eval

## Lazy histograms

*Lazy* histograms are simpler interfaces to the histograms, their are designed to be litgher in memory and faster in usage, but with limited capabilities. They are recommended when filling the histograms from a data sources when speed is an imporant factor.

## Ghost histograms

*Ghost* histograms have the same interface as lazy histograms, but do nothing. They are intended as a way to avoid time-expensive `if` checks when filling several histograms by filling the non interesting data into a `ghosthistogram` directly.

## Output files

# Development status

## Analytics

- >> All badges 

## Caveats

Some part of the code have a *non-pythonic* taste for several reasons:

- Adaptation of non python code from other physics data analysis tools
- Compatibility with early version of the code
- Practicality beats purity

The goal is to develop the module under the hood and improve it's performance, portabilty, simplicity. 

Any comments and suggestions are helpful.

## Authors

* **Greg Henning** - ghenning&#8203;*.at.*&#8203;iphc&#x2024;cnrs&#x2024;fr

## License

This project is licensed under the CeCILL FREE SOFTWARE LICENSE AGREEMENT. 

See [LICENSE](LICENSE) for more.

