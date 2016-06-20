"""
SpaceNet on Jimura et al "mixed gambles" dataset.
==================================================

The segmenting power of SpaceNet is quite visible here.

See also the SpaceNet documentation: :ref:`space_net`.
"""
# author: DOHMATOB Elvis Dopgima,
#         GRAMFORT Alexandre


##########################################################################
# Load the data from the Jimura mixed-gamble experiment
from nilearn.datasets import fetch_mixed_gambles
data = fetch_mixed_gambles(n_subjects=16)

zmap_filenames = data.zmaps
behavioral_target = data.gain
mask_filename = data.mask_img


from nilearn.plotting import plot_stat_map, show
from nilearn.decoding import SpaceNetRegressor
import time

for penalty in ('tv-l1', 'graph-net', 'social'):
    decoder = SpaceNetRegressor(mask=mask_filename, penalty=penalty,
                                eps=1e-1, verbose=10,
                                memory="nilearn_cache")

    t0 = time.time()
    decoder.fit(zmap_filenames, behavioral_target)
    elapsed = time.time() - t0
    title = "%s; time: %.1fs" % (penalty, elapsed)

    # Visualize weights
    display = plot_stat_map(decoder.coef_img_, title=title,
                            display_mode="yz", cut_coords=[20, -2])
    display.savefig('poldrack_%s.png' % penalty)

show

