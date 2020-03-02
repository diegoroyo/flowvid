# `flowvid` overview

* [Input](#input)
* [Data manipulation](#data-manipulation)
  * [Flow normalization and conversion to RGB](#flow-normalization-and-conversion-to-rgb)
  * [Endpoint error normalization and conversion to RGB](#endpoint-error-normalization-and-conversion-to-rgb)
  * [Track a given set of points using optical flow](#track-a-given-set-of-points-using-optical-flow)
* [Output](#output)

## Input

* `fv.input.flo(path)`: Read `.flo` files from path (file or directory).
* `fv.input.rgb(path)`: Read `.png`, `.jpg` or `.bmp` files from path (file or directory).
* `fv.input.rect(path)`: Read rectangle data from a text file.
* `fv.input.points(array)`: Read point data from a (x, y) point array.
* `fv.input.prompt_points(N, image)`: Let the user choose N points in an image in an interactive way.

```python
import flowvid as fv

# Get first 100 .flo files from directory
flo_data = fv.input.flo('path/to/flo', dir_total=100)

# Skip first 9 images from rgb directory
images = fv.input.rgb('path/to/rgb', dir_first=10)

# You can iterate through data
for image in images:
    print('Pixel (0,0) is', image[0, 0, :])

flo_data[0] # [height, width, 2] numpy ndarray of first flo file
```

```python
import flowvid as fv
import random

# (...)
first_image = images[0]
[h, w] = first_image.shape[0:2]

# Random point generation examples
n_points = 100
custom_points = np.reshape([[random.randrange(0, w - 1), random.randrange(0, h - 1)]
                             for i in range(n_points)], (n_points, 2))
points1 = fv.input.points(custom_points)

# Other options: interactive
points2 = fv.input.prompt_points(n_points, first_image)
```

## Data manipulation

_Note: operations described here might have additional paramters of customization, check its docstring._

* `fv.normalize_frame(data)`: Normalize flow/epe data (so module ranges from 0..1 instead of 0..n) with each frame's local maximum.
* `fv.normalize_video(data, clamp_pct, gamma)`: Normalize flow/epe (so module ranges from 0..1 instead of 0..n) with the video's maximum. Can also apply a gamma curve with clamping to compensate if there's a high point.
* `fv.accumulate(flow)`: Accumulate optical flow from first frame, so instead of it being from images 0->1, 1->2, 2->3, etc. it goes from images 0->1, 0->2, 0->3, etc.
---
* `fv.flow_to_rgb(flow)`: Convert flow data to RGB using Middlebury's color circle representation.
* `fv.epe_to_rgb(epe)`: Convert EPE data to RGB, where brighter colors mean that the error is bigger on that point.
---
* `fv.draw_rectangle(image, rect, color)`: Draw each rectangle in its corresponding image.
* `fv.draw_points(image, points, color, num_trail)`: Draw each set of points in its corresponding image. Draw a line across the `num_trail` last sets of points.
* `fv.add_flow_rect(rect, flow)`: Move the first rectangle according to the optical flow on the rectangle's points.
* `fv.add_flow_points(points, flow)`: Move the first set of points according to the optical flow.
* `fv.endpoint_error(flow_est, flow_gt)`: Calculate endpoint error for the given estimated and ground truth data.
* `fv.track_from_first(point_data, image_data, color)`: Put first image and first set of points side-by-side with the current frame to see how points are tracked.

### Flow normalization and conversion to RGB

```python
import flowvid as fv

flo_data = fv.input.flo('path/to/flo')

# You can normalize by frame OR the whole video
# Normalize each flo file independently
flo_frame = fv.normalize_frame(flo_data)
# Normalize all flo files at once, applying a clamp/gamma curve
flo_video = fv.normalize_video(flo_data, clamp_pct=0.8, gamma=1.5)

# Conversion from flow data to RGB
rgb_frames = fv.flow_to_rgb(flo_video)
```

### Endpoint error normalization and conversion to RGB

```python
import flowvid as fv

# Estimated and ground truth flow data
flo_est_data = fv.input.flo('path/to/est/flo')
flo_gt_data = fv.input.flo('path/to/gt/flo')

# Calculate endpoint error
epe_data = fv.endpoint_error(flo_est_data, flo_gt_data)

# You can normalize by frame OR the whole video
# Normalize each EPE independently
epe_frame = fv.normalize_frame(epe_data)
# Normalize all EPE at once, applying a clamp/gamma curve
epe_video = fv.normalize_video(epe_data, clamp_pct=0.8, gamma=1.5)

# Conversion from flow data to RGB
rgb_frames = fv.epe_to_rgb(epe_video)
```

### Track a given set of points using optical flow

```python
import flowvid as fv

# Read flow data and RGB frames corresponding to the video
flo_data = fv.input.flo('path/to/flo')
rgb_data = fv.input.rgb('path/to/rgb')

# Obtain some points to track
points = fv.input.prompt_points(5, rgb_data[0])

# Move the points using optical flow
points = fv.add_flow_points(points, flo_data)

# Two options:
# Move points in the video
track_image1 = fv.draw_points(rgb_data, points, color='random', num_trail=4)
# Put first frame side-by-side to see how points are moving
track_image2 = fv.track_from_first(points, rgb_data)
```

## Output

You can save your work as a video or as an image sequence, or show it in an interactive pyplot:

* `fv.output.video(path, framerate)`: Save as a video with given framerate
* `fv.output.image(path, name_format, first_id)`: Save as image sequence (see example)
* `fv.output.show_plot(title)`: Show interactive pyplot with video results sequence

```python
import flowvid as fv

# (...)
rgb_frames = fv.flow_to_rgb(flo_video)

# Option 1: Save as video
out1 = fv.output.video(filename='output.mp4', framerate=24)
out1.add_all(rgb_frames, verbose=True) # verbose adds a progress bar

# Option 2: Save as video (another, more complicated way)
out2 = fv.output.video(filename='output2.mp4')
for frame in rgb_frames:
    out2.add_frame(frame)

# Option 3: Save as image sequence
out3 = fv.output.image('path/to/dir', name_format='{:04}.png', first_id=1000)
out3.add_all(rgb_frames) # save 1000.png, 1001.png to (1000+n).png

# Option 4: Show interactive pyplot with images
out4 = fv.output.show_plot(title='Flow colors', framerate=10)
out4.show_all(rgb_frames, show_count=True)
```
