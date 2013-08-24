"""
"""
import time
import numpy as np
from sklearn.feature_selection import SelectPercentile

if 0:
    ### Load haxby dataset ########################################################

    from nisl import datasets
    dataset = datasets.fetch_haxby()

    ### Load Target labels ########################################################

    import sklearn.utils.fixes
    # Load target information as string and give a numerical identifier to each
    labels = np.loadtxt(dataset.session_target[0], dtype=np.str, skiprows=1,
                        usecols=(0,))

    # For compatibility with numpy 1.3 and scikit-learn 0.12
    # "return_inverse" option appeared in numpy 1.4, scikit-learn >= 0.14 supports
    # text labels.
    # With scikit-learn >= 0.14, replace this line by: target = labels
    _, target = sklearn.utils.fixes.unique(labels, return_inverse=True)

    ### Remove resting state condition ############################################

    conditions = np.recfromtxt(dataset.session_target[0], names=True)['labels']
    condition_mask = np.logical_or(conditions == 'face', conditions == 'house')

    ### Load the mask #############################################################

    from nisl.io import NiftiMasker
    nifti_masker = NiftiMasker(memory='nisl_cache',
                            memory_level=2, )#mask=dataset.mask_vt[0])

    # We give to the nifti_masker a filename, and retrieve a 2D array ready
    # for machine learning with scikit-learn
    fmri_masked = nifti_masker.fit_transform(dataset.func[0])

    ### Prediction function #######################################################

    # First, we remove rest condition
    X = fmri_masked[condition_mask, ...]
    y = target[condition_mask]
    X = SelectPercentile(percentile=30).fit_transform(X, y)
    np.save('X.npy', X)
    np.save('y.npy', y)
else:
    X = np.load('X.npy')
    y = np.load('y.npy')

# Here we use a Support Vector Classification, with a linear kernel and C=1
from sklearn.linear_model.logistic import logistic_regression, \
        LogisticRegression, logistic_regression_path, \
        LogisticRegressionCV

from sklearn.linear_model.logistic import _logistic_loss_and_grad
y_ = np.sign(y - y.mean())
X_center = X - X.mean(axis=0)
#X_center /= X.std(axis=0)

Cs = np.logspace(-4, 4, 20)

if 1:
    t0 = time.time()
    w_lbfgs = logistic_regression(X_center, y, C=1., #verbose=10,
                                  solver='lbfgs')
    t_lbfgs = time.time() - t0

    t0 = time.time()
    w_newton = logistic_regression(X_center, y, C=1., #verbose=10,
                             solver='lbfgs')
    t_newton = time.time() - t0

    log_reg = LogisticRegression(C=1., fit_intercept=False, )

    t0 = time.time()
    log_reg.fit(X_center, y)
    t_liblinear = time.time() - t0
    w_liblin = log_reg.coef_

    log_reg_d = LogisticRegression(C=1., fit_intercept=False, dual=True)

    t0 = time.time()
    log_reg_d.fit(X_center, y)
    t_liblin_d = time.time() - t0
    w_liblin_d = log_reg_d.coef_

    print 'Liblinear solver: time %.2fs, cost %.4e' % (t_liblinear,
            _logistic_loss_and_grad(w_liblin.squeeze(), X_center, y_,
                        1./1000)[0])
    print 'Liblinear solver dual: time %.2fs, cost %.4e' % (t_liblin_d,
            _logistic_loss_and_grad(w_liblin_d.squeeze(), X_center,
                        y_, 1./1000)[0])

    print 'L-BFGS solver: time %.2fs, cost %.4e' % (t_lbfgs,
            _logistic_loss_and_grad(w_lbfgs, X_center, y_, 1.)[0])

    print 'Newton solver: time %.2fs, cost %.4e' % (t_newton,
            _logistic_loss_and_grad(w_newton, X_center, y_, 1.)[0])



###############################################################################
print 'Comparing path'

if 1:
    t0 = time.time()
    log_reg_cv = LogisticRegressionCV(fit_intercept=True,
                                      Cs=Cs, solver='newton')
    log_reg_cv.fit(X, y)
    t_cv = time.time() - t0
    print "Full CV Newton: time: %.2f" % t_cv

if 1:
    t0 = time.time()
    log_reg_cv = LogisticRegressionCV(fit_intercept=True,
                                      Cs=Cs, solver='lbfgs')
    log_reg_cv.fit(X, y)
    t_cv = time.time() - t0
    print "Full CV l_bfgs: time: %.2f" % t_cv


if 1:
    t0 = time.time()
    for C in Cs:
        LogisticRegression(C=C, fit_intercept=True).fit(X, y)
    t_liblinear = time.time() - t0
    print 'Liblinear path: time %.2fs' % t_liblinear


if 0:
    log_reg = LogisticRegression(C=1., fit_intercept=True, )

    t0 = time.time()
    log_reg.fit(X_center, y)
    t_liblinear = time.time() - t0
    w_liblin = log_reg.coef_

    log_reg_d = LogisticRegression(C=1., fit_intercept=True, dual=True)

    t0 = time.time()
    log_reg_d.fit(X_center, y)
    t_liblin_d = time.time() - t0
    w_liblin_d = log_reg_d.coef_

    print 'Liblinear solver: time %.2fs, cost %.4e' % (t_liblinear,
            _logistic_loss_and_grad(w_liblin.squeeze(), X_center,
                                    y_, 1./1000)[0])
    print 'Liblinear solver dual: time %.2fs, cost %.4e' % (t_liblin_d,
            _logistic_loss_and_grad(w_liblin_d.squeeze(), X_center,
                                    y_, 1./1000)[0])


