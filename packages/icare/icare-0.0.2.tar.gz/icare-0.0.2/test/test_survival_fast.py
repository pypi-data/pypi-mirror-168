from sklearn.utils.estimator_checks import check_estimator
from sksurv import datasets
from sksurv.preprocessing import OneHotEncoder

from icare.metrics import *
from icare.survival import IcareSurv, BaggedIcareSurv


def generate_random_param_set():
    return {
        'rho': np.random.uniform(0.01, 1.),
        'correlation_method': np.random.choice(['spearman', 'pearson']),
        'sign_method': np.random.choice(['harrell', 'tAUC', 'uno'],
                                        np.random.randint(1, 4),
                                        replace=False).tolist(),
        'cmin': np.random.uniform(0.5, 1.),
        'max_features': np.random.uniform(0.5, 1.),
        'random_state': None,
    }


def generate_random_param_set_bagged():
    return {
        'n_estimators': np.random.randint(1, 10),
        'parameters_sets': [generate_random_param_set() for x in range(np.random.randint(1, 3))],
        'aggregation_method': np.random.choice(['mean', 'median']),
        'n_jobs': np.random.randint(1, 5),
        'random_state': None,
    }


def test_feature_sign():
    X, y = datasets.load_veterans_lung_cancer()
    X = OneHotEncoder().fit_transform(X)

    ml = BaggedIcareSurv(n_estimators=50,
                         n_jobs=-1,
                         parameters_sets=[{'max_features':1,
                                           'rho' : None,
                                           'cmin': 0.5}])
    ml.fit(X, y)
    fs = ml.average_feature_signs_
    fs_kar = fs[fs['feature']=='Karnofsky_score']['average sign'].values[0]
    fs_celltype = fs[fs['feature']=='Celltype=smallcell']['average sign'].values[0]
    assert fs_kar < 0
    assert fs_celltype > 0



def test_feature_group():
    X, y = datasets.load_aids(endpoint='death')
    X = OneHotEncoder().fit_transform(X)

    ml = IcareSurv()
    ml.fit(X, y)

    feature_groups = None
    ml.fit(X, y, feature_groups=feature_groups)

    ml = IcareSurv(features_groups_to_use=[0, 1])
    feature_groups = np.ones(int(X.shape[1] / 2))
    feature_groups = np.concatenate([feature_groups, np.zeros(X.shape[1] - len(feature_groups))])
    ml.fit(X, y, feature_groups=feature_groups)
    harrell_cindex_scorer(ml, X, y)


def test_scikit_simple():
    check_estimator(IcareSurv())


def test_scikit_bagged():
    check_estimator(BaggedIcareSurv())


def test_no_censoring():
    X, y = datasets.load_veterans_lung_cancer()
    X = OneHotEncoder().fit_transform(X)

    ml = IcareSurv()
    ml.fit(X, y)

    y = [x[1] for x in y]
    ml.fit(X, y)


def test_scorer():
    X, y = datasets.load_veterans_lung_cancer()
    X = OneHotEncoder().fit_transform(X)

    ml = IcareSurv()
    ml.fit(X, y)
    harrell_cindex_scorer(ml, X, y)
    uno_cindex_scorer(ml, X, y)
    tAUC_scorer(ml, X, y)
