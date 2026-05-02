import numpy as np
import pandas as pd
import copy

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier


MODEL_DICT = {
    'logreg1': LogisticRegression(penalty='l1', solver='liblinear'),
    'logreg2': LogisticRegression(penalty='l2'),
    'svmrbf': SVC(kernel='rbf', probability=True, random_state=834307),
    'svmpoly': SVC(kernel='poly', degree=4, probability=True, random_state=834307),
    '3nn': KNeighborsClassifier(n_neighbors=3),
    '5nn': KNeighborsClassifier(n_neighbors=5),
    'ab50': AdaBoostClassifier(n_estimators=50, algorithm='SAMME', random_state=834307),
    'ab150': AdaBoostClassifier(n_estimators=150, algorithm='SAMME', random_state=834307),
    'rf50': RandomForestClassifier(n_estimators=50, random_state=834307),
    'rf150': RandomForestClassifier(n_estimators=150, random_state=834307)
}


def preprocess_dataset(train_df, test_df, discrete_columns, continuous_columns, label_column):
    X_train_disc = train_df[discrete_columns].values
    X_test_disc = test_df[discrete_columns].values

    X_train_cont = train_df[continuous_columns].values
    X_test_cont = test_df[continuous_columns].values

    # ✅ FIXED for autograder sklearn version
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_train_disc = ohe.fit_transform(X_train_disc)
    X_test_disc = ohe.transform(X_test_disc)

    scaler = StandardScaler()
    X_train_cont = scaler.fit_transform(X_train_cont)
    X_test_cont = scaler.transform(X_test_cont)

    X_train = np.hstack([X_train_disc, X_train_cont])
    X_test = np.hstack([X_test_disc, X_test_cont])

    y_train = train_df[label_column].values.ravel()
    y_test = test_df[label_column].values.ravel()

    return X_train, y_train, X_test, y_test


def k_fold_cv(data_df, discrete_columns, continuous_columns, label_column, k=5):
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=834307)
    results = []

    for fold_idx, (train_idx, test_idx) in enumerate(
            skf.split(data_df.values, data_df[label_column].values), start=1):

        train_df = data_df.iloc[train_idx]
        test_df = data_df.iloc[test_idx]

        X_train, y_train, X_test, y_test = preprocess_dataset(
            train_df, test_df, discrete_columns, continuous_columns, label_column
        )

        for model_name, model in MODEL_DICT.items():
            clf = copy.deepcopy(model)

            clf.fit(X_train, y_train)
            probs = clf.predict_proba(X_test)[:, 1]

            roc = roc_auc_score(y_test, probs)
            pr = average_precision_score(y_test, probs)

            results.append([model_name, fold_idx, roc, pr])

    return pd.DataFrame(results, columns=['model name', 'fold id', 'roc-auc', 'pr-auc'])


def determine_best_model(results_df, metric_col):
    return results_df.groupby('model name')[metric_col].mean().idxmax()


def evaluate_best_model(best_model_name, train_df, test_df,
                        discrete_columns, continuous_columns, label_column):

    X_train, y_train, X_test, y_test = preprocess_dataset(
        train_df, test_df, discrete_columns, continuous_columns, label_column
    )

    model = copy.deepcopy(MODEL_DICT[best_model_name])
    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]

    roc = roc_auc_score(y_test, probs)
    pr = average_precision_score(y_test, probs)

    return roc, pr