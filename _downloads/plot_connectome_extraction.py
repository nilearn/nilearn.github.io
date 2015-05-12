"""
Extracting signals of a probabilistic atlas of rest functional regions
========================================================================

This examples shows how to extract the signal on regions defined via a
probabilistic atlas, for construction of a functional
connectome.

We use the `MSDL atlas
<https://team.inria.fr/parietal/research/spatial_patterns/spatial-patterns-in-resting-state/>`_
of functional regions in rest.

The key to extract signals is to use the
:class:`nilearn.input_data.NiftiMapsMasker` that can transform nifti
objects to time series using a probabilistic atlas.

"""

from nilearn import datasets
atlas = datasets.fetch_msdl_atlas()
atlas_filename = atlas['maps']

# Load the labels
import numpy as np
csv_filename = atlas['labels']

# The recfromcsv function can load a csv file
labels = np.recfromcsv(csv_filename)
names = labels['name']

from nilearn.input_data import NiftiMapsMasker
masker = NiftiMapsMasker(maps_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)

data = datasets.fetch_adhd(n_subjects=1)

time_series = masker.fit_transform(data.func[0],
                                   confounds=data.confounds)

correlation_matrix = np.corrcoef(time_series.T)

# Display the correlation matrix
from matplotlib import pyplot as plt
plt.figure(figsize=(10, 10))
plt.imshow(correlation_matrix, interpolation="nearest")
# And display the labels
x_ticks = plt.xticks(range(len(names)), names, rotation=90)
y_ticks = plt.yticks(range(len(names)), names)

# And now display the corresponding graph
from nilearn import plotting
coords = np.vstack((labels['x'], labels['y'], labels['z']))

# We threshold to keep only the 20% of edges with the highest value
# because the graph is very dense
plotting.plot_connectome(correlation_matrix, coords.T,
                         edge_threshold="80%")

plt.show()


