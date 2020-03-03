<p align="center">
  <a href="https://github.com/diegoroyo/flowvid">
    <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/logo_square.png" alt="Logo" width=250 height=250>
  </a>

  <p align="center">
    Toolkit to generate customized visualizations related to optical flow <i>(beta 0.2.1)</i>
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
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/color_flow.png" alt="color_flow result"></td>
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/color_epe.png" alt="color_epe result"></td>
<td align="center"><img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/track_points.png" alt="track_points result"></td>
</tr>
</table>

## Table of contents

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

## Quick start

Flowvid is a python library for video generation, but it also contains several video presets with an user-friendly assistant:

* Presets can be listed using `python3 -m flowvid -h`

```
$ python3 -m flowvid -h

usage: flowvid [-h] preset

Generate an optical flow visualization using the available presets.

Preset can be one of:
  color_flow: Convert flow data to RGB using the Middlebury representation
  color_epe: Calculate endpoint error and generate a video representation
  plot_epe: Generate a pyplot plot with the EPE distribution in all frames
  track_points: Place points in a image and see how flow moves them
  track_side_by_side: Place points in a image and see how flow can track them

positional arguments:
  preset      Video preset, see above.

optional arguments:
  -h, --help  show this help message and exit
```

* Example: converting flow files to rgb and saving into a video

```
$ python3 -m flowvid color_flow

Flow files directory (default: flo): path/to/flo/dir 
Vector normalize type (video, [frame], none): video
Normalization clamp percentage (default: 1.0): 0.8
Normalization gamma curve exponent (default: 1.0): 1.5
Video framerate (default: 24): 12
Output video name (default: output_color_flow.mp4): flowcolors.mp4 
```
<p align="center">
<img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/color_flow.png" alt="color_flow result">
</p>

Here are some examples illustrating the other presets' results:

| **`color_epe`** | **`plot_epe`** |
|---|---|
| <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/color_epe.png" alt="color_epe result"> | <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/plot_epe.png" alt="plot_epe result"> |

| **`track_points`** | **`track_side_by_side`** |
|---|---|
| <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/track_points.png" alt="track_points result"> | <img src="https://raw.githubusercontent.com/diegoroyo/flowvid/master/examples/track_side_by_side.png" alt="track_side_by_side result"> |

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