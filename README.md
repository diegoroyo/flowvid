<p align="center">
  <!-- <a href="https://github.com/diegoroyo/flowvid">
    <img src="https://via.placeholder.com/72" alt="Logo" width=72 height=72>
  </a> -->

  <h1 align="center">flowvid</h1>

  <p align="center">
    Toolkit to generate customized visualizations related to optical flow <i>(beta 0.1.0)</i>
    <br>
    <!-- <a href="https://TODO">PyPI page</a>
    · -->
    <a href="https://github.com/diegoroyo/flowvid/blob/master/README.md#installation">Installation</a>
    ·
    <a href="https://github.com/diegoroyo/flowvid/blob/master/examples">Examples</a>
  </p>
</p>


## Table of contents

- [Installation](#installation)
- [Quick start](#quick-start)
    - [Python library](#python-library)
- [Acknowledgements](#acknowledgements)


## Installation

For now installation is only available from Github:

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

positional arguments:
  preset      Preset, one of: (color_flow)

optional arguments:
  -h, --help  show this help message and exit
```

* Example: converting flow files to rgb and saving into a video

```
$ python3 -m flowvid color_flow

Flow files directory (default: flo): path/to/flo/dir 
Vector normalize type (video, [frame], none): video
Normalization clamp percentage (default: 1.0): 0.8
Normalization gamma curve exponent (default: 1.0): 0.7
Video framerate (default: 24): 12
Output video name (default: output_flo.mp4): flowcolors.mp4 
```

### Python library

If you want to generate more complex or customized videos, you can easily use `flowvid`'s tools:

* You can check the [documentation and example usages here](https://github.com/diegoroyo/flowvid/blob/master/examples).

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

Flow to RGB conversion is based on [C. Liu's work](https://people.csail.mit.edu/celiu/OpticalFlow/).

> C. Liu. Beyond Pixels: Exploring New Representations and Applications for Motion Analysis. Doctoral Thesis. Massachusetts Institute of Technology. May 2009.