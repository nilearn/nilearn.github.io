0.6.0a
======

**Released October 2019**

NEW
---

.. warning::

 | **Python2 and 3.4 are no longer supported. We recommend upgrading to Python 3.6 minimum.**
 |
 | **Minimum supported versions of packages have been bumped up.**
 | - Matplotlib -- v2.0
 | - Scikit-learn -- v0.19
 | - Scipy -- v0.19

- A new method for :class:`nilearn.input_data.NiftiMasker` instances
  for generating reports viewable in a web browser, Jupyter Notebook, or VSCode.

- joblib is now a dependency

- Parcellation method ReNA: Fast agglomerative clustering based on recursive
  nearest neighbor grouping.
  Yields very fast & accurate models, without creation of giant
  clusters.
  :class:`nilearn.regions.ReNA`
- Plot connectome strength
  Use :func:`nilearn.plotting.plot_connectome_strength` to plot the strength of a
  connectome on a glass brain.  Strength is absolute sum of the edges at a node.
- Optimization to image resampling
  :func:`nilearn.image.resample_img` has been optimized to pad rather than
  resample images in the special case when there is only a translation
  between two spaces. This is a common case in :class:`nilearn.input_data.NiftiMasker`
  when using the `mask_strategy="template"` option for brains in MNI space.
- New brain development fMRI dataset fetcher
  :func:`nilearn.datasets.fetch_development_fmri` can be used to download
  movie-watching data in children and adults. A light-weight dataset
  implemented for teaching and usage in the examples.
- New example in `examples/05_advanced/plot_age_group_prediction_cross_val.py`
  to compare methods for classifying subjects into age groups based on
  functional connectivity. Similar example in
  `examples/03_connectivity/plot_group_level_connectivity.py` simplified.

- Merged `examples/03_connectivity/plot_adhd_spheres.py` and
  `examples/03_connectivity/plot_sphere_based_connectome.py` to remove
  duplication across examples. The improved
  `examples/03_connectivity/plot_sphere_based_connectome.py` contains
  concepts previously reviewed in both examples.
- Merged `examples/03_connectivity/plot_compare_decomposition.py`
  and `examples/03_connectivity/plot_canica_analysis.py` into an improved
  `examples/03_connectivity/plot_compare_decomposition.py`.

- The Localizer dataset now follows the BIDS organization.


Changes
-------

- All the connectivity examples are changed from ADHD to brain development
  fmri dataset.

- :func:`nilearn.plotting.view_img_on_surf`, :func:`nilearn.plotting.view_surf`
  and :func:`nilearn.plotting.view_connectome` now allow disabling the colorbar,
  and setting its height and the fontsize of its ticklabels.

- :func:`nilearn.plotting.view_img_on_surf`, :func:`nilearn.plotting.view_surf`
  and :func:`nilearn.plotting.view_connectome` can now display a title.

- Rework of the standardize-options of :func:`nilearn.signal.clean` and the various Maskers
  in `nilearn.input_data`. You can now set `standardize` to `zscore` or `psc`. `psc` stands
  for `Percent Signal Change`, which can be a meaningful metric for BOLD.

- :func:`nilearn.plotting.plot_img` now has explicit keyword arguments `bg_img`,
  `vmin` and `vmax` to control the background image and the bounds of the
  colormap. These arguments were already accepted in `kwargs` but not documented
  before.

- :func:`nilearn.plotting.view_connectome` now converts NaNs in the adjacency
  matrix to 0.

- Removed the plotting connectomes example which used the Seitzman atlas
  from `examples/03_connectivity/plot_sphere_based_connectome.py`.
  The atlas data is unsuitable for the method & the example is redundant.

Fixes
-----

- :func:`nilearn.plotting.plot_glass_brain` with colorbar=True does not crash when
  images have NaNs.
- add_contours now accepts `threshold` argument for filled=False. Now
  `threshold` is equally applied when asked for fillings in the contours.
- :func:`nilearn.plotting.plot_surf` and
  :func:`nilearn.plotting.plot_surf_stat_map` no longer threshold zero values
  when no threshold is given.
- When :func:`nilearn.plotting.plot_surf_stat_map` is used with a thresholded map
  but without a background map, the surface mesh is displayed in
  half-transparent grey to maintain a 3D perception.
- :func:`nilearn.plotting.view_surf` now accepts surface data provided as a file
  path.
- :func:`nilearn.plotting.plot_glass_brain` now correctly displays the left 'l' orientation even when
  the given images are completely masked (empty images).
- :func:`nilearn.plotting.plot_matrix` providing labels=None, False, or an empty list now correctly disables labels.
- :func:`nilearn.plotting.plot_surf_roi` now takes vmin, vmax parameters
- :func:`nilearn.datasets.fetch_surf_nki_enhanced` is now downloading the correct
  left and right functional surface data for each subject
- :func:`nilearn.datasets.fetch_atlas_schaefer_2018` now downloads from release
  version 0.14.3 (instead of 0.8.1) by default, which includes corrected region label
  names along with 700 and 900 region parcelations.
- Colormap creation functions have been updated to avoid matplotlib deprecation warnings
  about colormap reversal.
- Neurovault fetcher no longer fails if unable to update dataset metadata file due to faulty permissions.

Contributors
------------

The following people contributed to this release (in alphabetical order)::

	Alexandre Abraham
	Alexandre Gramfort
	Ana Luisa
	Ana Luisa Pinho
	Andrés Hoyos Idrobo
	Antoine Grigis
	BAZEILLE Thomas
	Bertrand Thirion
	Colin Reininger
	Céline Delettre
	Dan Gale
	Daniel Gomez
	Elizabeth DuPre
	Eric Larson
	Franz Liem
	Gael Varoquaux
	Gilles de Hollander
	Greg Kiar
	Guillaume Lemaitre
	Ian Abenes
	Jake Vogel
	Jerome Dockes
	Jerome-Alexis Chevalier
	Julia Huntenburg
	Kamalakar Daddy
	Kshitij Chawla (kchawla-pi)
	Mehdi Rahim
	Moritz Boos
	Sylvain Takerkart
