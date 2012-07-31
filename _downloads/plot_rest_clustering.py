"""
Hierachical clustering to learn a brain parcellation from rest fMRI
====================================================================

We use spatial-constrained Ward-clustering to create a set of
parcels. These parcels are particularly interesting for creating a
'compressed' representation of the data, replacing the data in the fMRI
images by mean on the parcellation.

This parcellation may be useful in a supervised learning, see for
instance: `A supervised clustering approach for fMRI-based inference of
brain states <http://hal.inria.fr/inria-00589201>`_, Michel et al,
Pattern Recognition 2011.

"""

### Load nyu_rest dataset #####################################################

from nisl import datasets
dataset = datasets.fetch_nyu_rest(n_subjects=1)

### Mask ######################################################################

fmri_data = dataset.func[0]

# Compute a brain mask
from nisl import masking
mask = masking.compute_mask(fmri_data)

# Mask data: go from a 4D dataset to a 2D dataset with only the voxels
# in the mask
fmri_masked = fmri_data[mask]

### Ward ######################################################################

# Compute connectivity matrix: which voxel is connected to which
from sklearn.feature_extraction import image
shape = mask.shape
connectivity = image.grid_to_graph(n_x=shape[0], n_y=shape[1],
                                   n_z=shape[2], mask=mask)

# Computing the ward for the first time, this is long...
from sklearn.cluster import WardAgglomeration
import time
start = time.time()
ward = WardAgglomeration(n_clusters=5000, connectivity=connectivity,
                         )#memory='nisl_cache')
ward.fit(fmri_masked.T)
print "Ward agglomeration 500 clusters: %.2fs" % (time.time() - start)

