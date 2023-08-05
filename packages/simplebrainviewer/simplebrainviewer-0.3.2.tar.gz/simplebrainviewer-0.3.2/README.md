# SimpleBrainViewer
A simple brain viewer using matplotlib

###### What is this?
Pretty self-explanatory... It's a simple brain viewer written
with matplotlib. Useful if you just want to view a volume quickly
directly in python.

###### Usage

You can call the BrainViewer from python or the command line (via nifti file or any other nibabel compatible format):

```python
import nibabel as nib
import simplebrainviewer as sbv

# load a volume
img = nib.load('/a/nifti/file')

# plot the img
sbv.plot_brain(img)

# you can also display numpy arrays
sbv.plot_brain(img.get_fdata())

```

###### Command Line Usage
```
usage: sbv [-h] volume

View a brain volume

positional arguments:
  volume      brain volume to view

options:
  -h, --help  show this help message and exit
```

