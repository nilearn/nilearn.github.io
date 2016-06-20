"""
Decoding with SpaceNet: face vs house object recognition
=========================================================

Here is a simple example of decoding with a SpaceNet prior (i.e Graph-Net,
TV-l1, etc.), reproducing the Haxby 2001 study on a face vs house
discrimination task.

See also the SpaceNet documentation: :ref:`space_net`.
"""

##############################################################################
# Load the Haxby dataset
from nilearn.datasets import fetch_haxby
data_files = fetch_haxby()

# Load Target labels
import numpy as np
labels = np.recfromcsv(data_files.session_target[0], delimiter=" ")


# Restrict to face and house conditions
target = labels['labels']
condition_mask = np.logical_or(target == b"face", target == b"house")

# Split data into train and test samples, using the chunks
condition_mask_train = np.logical_and(condition_mask, labels['chunks'] <= 6)
condition_mask_test = np.logical_and(condition_mask, labels['chunks'] > 6)

# Apply this sample mask to X (fMRI data) and y (behavioral labels)
# Because the data is in one single large 4D image, we need to use
# index_img to do the split easily
from nilearn.image import index_img
func_filenames = data_files.func[0]
X_train = index_img(func_filenames, condition_mask_train)
X_test = index_img(func_filenames, condition_mask_test)
y_train = target[condition_mask_train]
y_test = target[condition_mask_test]

##############################################################################
# Fit SpaceNet with a Social sparsity penalty
from nilearn.decoding import SpaceNetClassifier
from nilearn.plotting import plot_stat_map, show
import time

for penalty in ('tv-l1', 'graph-net', 'social'):
    # Fit model on train data and predict on test data
    decoder = SpaceNetClassifier(memory="nilearn_cache", penalty='social',
                                verbose=10,
                                screening_percentile=50)
    t0 = time.time()
    decoder.fit(X_train, y_train)
    elapsed = time.time() - t0
    y_pred = decoder.predict(X_test)
    accuracy = (y_pred == y_test).mean() * 100.
    title = "%s; time: %.1fs; accuracy: %g%%" % (penalty, elapsed, accuracy)

    # Visualization
    coef_img = decoder.coef_img_
    display = plot_stat_map(coef_img, data_files.anat[0],
                            title=title,
                            cut_coords=(23, -34, -16))
    display.savefig('haxby_%s.png' % penalty)

    # Save the coefficients to a nifti file
    coef_img.to_filename('haxby_%s_weights.nii' % penalty)

show()


###################################
# We can see that the TV-l1 penalty is 3 times slower to converge and
# gives the same prediction accuracy. However, it yields much
# cleaner coefficient maps

