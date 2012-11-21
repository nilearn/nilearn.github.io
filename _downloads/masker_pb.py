import numpy as np
import pylab as pl
cut_coord = 45

### Load ADHD rest dataset ####################################################
from nisl import datasets
# Here we use only 5 subjects to get faster-running code. For better
# results, simply increase this number
dataset = datasets.fetch_adhd()
func_files = dataset.func[:2]
confounds_files = dataset.regressor[:2]

from nisl import io

### NiftiMultiMasker ##########################################################
masker = io.NiftiMultiMasker(detrend=False,
                             memory="canica",
                             transform_memory="canica",
                             confounds=confounds_files, verbose=10)
data_masked = masker.fit_transform(func_files)

# XXX: screwed up API: the constructor is given data-dependent stuff:
# confounds

mean_epi = masker.inverse_transform(data_masked[0].mean(axis=0)).get_data()

pl.figure(figsize=(6, 3))
pl.subplot(1, 3, 1)
pl.imshow(np.rot90(mean_epi[:, :, cut_coord]), interpolation='nearest',
            cmap=pl.cm.gray)
pl.title('NiftiMultiMasker')
pl.axis('off')

### NiftiMasker ###############################################################
masker = io.NiftiMasker(memory="canica",
                        transform_memory="canica",
                        confounds=confounds_files[0], verbose=10)
data_masked = masker.fit_transform(func_files[0])
mean_epi = masker.inverse_transform(data_masked.mean(axis=0)).get_data()

pl.subplot(1, 3, 2)
pl.imshow(np.rot90(mean_epi[:, :, cut_coord]), interpolation='nearest',
            cmap=pl.cm.gray)
pl.title('NiftiMasker')
pl.axis('off')

### Manually ##################################################################
import nibabel
epi_img = nibabel.load(func_files[0])
mean_epi = epi_img.get_data().mean(axis=-1)

pl.subplot(1, 3, 3)
pl.imshow(np.rot90(mean_epi[:, :, cut_coord]), interpolation='nearest',
            cmap=pl.cm.gray)
pl.title('Manually')
pl.axis('off')

pl.show()
