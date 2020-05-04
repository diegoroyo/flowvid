<p align="center">
  <a href="https://github.com/diegoroyo/flowvid">
    <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/logo_square.png" alt="Logo" width=250 height=250>
  </a>

  <p align="center">
    <a href="https://badge.fury.io/py/flowvid"><img src="https://badge.fury.io/py/flowvid.svg" alt="PyPI version" height="18"></a>
    <a href="https://pepy.tech/project/flowvid/month"><img src="https://pepy.tech/badge/flowvid/month" alt="PyPI monthly downloads" height="18"></a>
    <a href="https://github.com/diegoroyo/flowvid/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/diegoroyo/flowvid" height="18"></a>
    <br>
    Toolkit to generate customized visualizations related to optical flow
    <br>
    <a href="https://pypi.org/project/flowvid/">PyPI page</a>
    ·
    <a href="https://github.com/diegoroyo/flowvid/blob/master/README.md#installation">Installation</a>
    ·
    <a href="https://github.com/diegoroyo/flowvid/blob/master/examples">Examples</a>
    ·
    <a href="https://github.com/diegoroyo/flowvid/blob/master/flowvid/presets">Presets</a>
  </p>
</p>

<table align="center">
<tr>
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/color_flow.png" alt="color_flow result"></td>
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/color_epe.png" alt="color_epe result"></td>
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/flow_arrows_1.png" alt="flow_arrows result"></td>
</tr>
</table>


## Table of contents

`flowvid` is a toolkit for all things related to optical flow. It comes with many visualization presets you can generate with no effort (see below), but it also allows for more complex data manipulation that doesn't have to imply generating a visualization (see [examples](https://github.com/diegoroyo/flowvid/blob/master/examples)).

- [Installation](#installation)
- [Quick start](#quick-start)
    - [Python library](#python-library)
- [Acknowledgements](#acknowledgements)


## Installation

`flowvid` is available as a PyPI package:
```
pip3 install flowvid
```
Or you can install it directly from Github:
```
pip3 install git+https://github.com/diegoroyo/flowvid/
```
or you can clone the repo:
```
git clone https://github.com/diegoroyo/flowvid.git
cd flowvid
scripts/local_install.sh
```

You might need to install the following dependencies:
```bash
pip3 install imageio imageio-ffmpeg numpy matplotlib Pillow
# or if you use the provided requirements.txt
pip3 install -r requirements.txt
```


## Quick start

Flowvid is a python library for video generation, but it also contains several video presets with an user-friendly assistant:

* Usage: `python3 -m flowvid `_`<preset>`_ `[ <config-params> | --config <config-file> ]`
* Presets can be listed using `python3 -m flowvid -h`

```
Preset can be one of:
  color_flow: Convert flow data to RGB using the Middlebury representation
  color_epe: Calculate endpoint error and generate a video representation
  flow_arrows: Draw arrows representing optical flow over a video
  plot_epe: Generate a pyplot plot with the EPE distribution in all frames
  track_points: Place points in a image and see how flow moves them
  track_side_by_side: Place points in a image and see how flow can track them
```

* Example: converting flow files to rgb and saving into a video

```bash
$ python3 -m flowvid color_flow

# \/ option names are shown here
[--flo-dir] Flow files directory (default: flo): path/to/flo/dir
[--norm-type] Vector normalization type (video, [frame], none): video
[--norm-clamp] Normalization clamp percentage (default: 1.0): 0.8
[--norm-gamma] Normalization gamma curve exponent (default: 1.0): 1.5
[--output-type] Output type ([video], pyplot): pyplot
[--output-framerate] Video framerate (default: 10): 10
```

You can specify its parameters via the command line. The following is equivalent:

```bash
# Option names can be listed with python3 -m flowvid --help
$ python3 -m flowvid color_flow
    --flo-dir path/to/flo/dir
    --norm-type video
    --norm-clamp 0.8
    --norm-gamma 1.5
    --output-type pyplot
    --output-framerate 10
```

Configuration can also be saved in a file so you don't have to type it always:

```bash
# Store configuration after use
$ python3 -m flowvid color_flow --flo-dir path/to/flo/dir (...)

Save configuration in a file? (y, [n]): y
Output configuration filename (default: preset_color_flow.yaml): path/to/config.yaml

Saved configuration file in path/to/config.yaml

(...)

# Load from a file
$ python3 -m flowvid color_flow --config path/to/config.yaml
```

<p align="center">
<img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/color_flow.png" alt="color_flow result">
</p>

Here are some examples illustrating the other presets' results:

| **`color_epe`** | **`plot_epe`** |
|---|---|
| <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/color_epe.png" alt="color_epe result"> | <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/plot_epe.png" alt="plot_epe result"> |

| **`track_points`** | **`track_side_by_side`** |
|---|---|
| <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/track_points.png" alt="track_points result"> | <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/track_side_by_side.png" alt="track_side_by_side result"> |

| **`flow_arrows`** (1) | **`flow_arrows`** (2) |
|---|---|
| <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/flow_arrows_1.png" alt="flow_arrows result"> | <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/images/flow_arrows_2.png" alt="flow_arrows result"> |

### Python library

If you want to generate more complex or customized videos, you can easily use `flowvid`'s tools:

* You can check the [documentation and example usages here](https://github.com/diegoroyo/flowvid/blob/master/examples).
* You can check the [source code for the given presets here](https://github.com/diegoroyo/flowvid/blob/master/flowvid/presets).

```python
import flowvid as fv

# Read flow files data
flo_data = fv.input.flo('path/to/flo/dir')

# Normalize each file (so max flow's module is 1),
# necessary to convert to RGB
flo_data = fv.normalize_frame(flo_data)
rgb_data = fv.flow_to_rgb(flo_data)

# Output as video
out = fv.output.video(filename='output.mp4', framerate=24)
out.add_all(rgb_data)
```


## Acknowledgements

* Logo made by Github user [Aeri (see profile)](https://github.com/aeri).

* Flow to RGB conversion is based on [C. Liu's work](https://people.csail.mit.edu/celiu/OpticalFlow/).

> C. Liu. Beyond Pixels: Exploring New Representations and Applications for Motion Analysis. Doctoral Thesis. Massachusetts Institute of Technology. May 2009.