# `flowvid` overview

* [Input](#input)
* [Data manipulation](#data-manipulation)
* [Output](#output)

## Input

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
* `fv.input.flo(path)`: Read `.flo` files from path (file or directory).
* `fv.input.rgb(path)`: Read `.png`, `.jpg` or `.bmp` files from path (file or directory).
* `fv.input.rect(path)`: Read rectangle data from a text file.

## Data manipulation

```python
import flowvid as fv

flo_data = fv.input.flo('path/to/flo')

# You can normalize by frame OR the whole video
# Normalize each flo file independently
flo_frame = fv.normalize_frame(flo_data)
# Normalize all flo files at once, applying a clamp/gamma curve
flo_video = fv.normalize_video(flo_data, clamp_pct=0.8, gamma=0.7)

# Conversion from flow data to RGB
rgb_frames = fv.flow_to_rgb(flo_video)
```

## Output

You can save your work as a video or as an image sequence

```python
import flowvid as fv

# (...)
rgb_frames = fv.flow_to_rgb(flo_video)

# Save as video
out = fv.output.video(filename='output.mp4', framerate=24)
out.add_all(rgb_frames, verbose=True) # verbose adds a progress bar

# Save as video (another, more complicated way)
out2 = fv.output.video(filename='output2.mp4')
for frame in rgb_frames:
    out2.add_frame(frame)

# Save as image sequence
out3 = fv.output.image('path/to/dir', name_format='{:04}.png', first_id=1000)
out3.add_all(rgb_frames) # save 1000.png, 1001.png to (1000+n).png
```