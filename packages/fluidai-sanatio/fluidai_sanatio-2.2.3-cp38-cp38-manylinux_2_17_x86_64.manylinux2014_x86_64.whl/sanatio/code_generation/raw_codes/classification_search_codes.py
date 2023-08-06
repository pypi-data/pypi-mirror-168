from sanatio.code_generation.raw_codes.metrics_codes import gini_index


def search_xgb_classification(X_train, X_test, y_train, y_test, train_gini_threshold=0.7, oot_gini_threshold=0.7,
                              n_iter=25, cv=5):
    from xgboost import XGBClassifier
    from sklearn.model_selection import RandomizedSearchCV
    import numpy as np
    import pandas as pd
    ###################### Add/Modify the search space below ###########################
    params = {
        'learning_rate': list(np.linspace(0.01, 0.1, 10)) + list(np.linspace(0.1, 0.5, 5)),
        'n_estimators': list(np.linspace(50, 500, 5, dtype=int)) + list(np.linspace(500, 1500, 10, dtype=int)),
        'subsample': list(np.linspace(0.5, 1, 5)) + [1],
        'min_child_weight': list(np.linspace(0, 1, 5)) + list(np.linspace(1, 200, 10)) + list(np.linspace(200, 600, 5)),
        'max_depth': [3, 4, 5],
        'scale_pos_weight': [1] + list(np.linspace(0.5, 2, 5)) + list(np.linspace(2, 20, 3)),
        'random_state': [42],
    }
    #####################################################################################
    # Initializing the random search with xgb model
    clf = RandomizedSearchCV(
        estimator=XGBClassifier(eval_metric="logloss", use_label_encoder=False, seed=42),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='roc_auc',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models over the parameter space defined above
    clf.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=0)
    # Storing the results in a dataframe
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_gini = []
    test_gini = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = XGBClassifier(**df_cv['params'][i])
        model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=0)
        # Getiing gini score
        train_gini.append(gini_index(y_train, model.predict(X_train)))
        test_gini_score = gini_index(y_test, model.predict(X_test))
        test_gini.append(test_gini_score)
        # Make a model best when it has the highest gini score
        if test_gini_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_gini, test_gini), columns=['train_gini', 'test/oot_gini'])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values('test/oot_gini', ascending=False)

    if (output_df['train_gini'] > train_gini_threshold).any() and (
            output_df['test/oot_gini'] > oot_gini_threshold).any():
        print("Search script was able to find xgboost models above {} train and {} test/oot_threshold".format(
            train_gini_threshold, oot_gini_threshold))
    else:
        print("No xgboost models were found that surpasses the given threshold")

    return best_model, output_df, clf.best_estimator_, clf


def search_random_forest_classification(X_train, X_test, y_train, y_test, train_gini_threshold=0.7,
                                        oot_gini_threshold=0.7, n_iter=25, cv=5):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import RandomizedSearchCV
    import numpy as np
    import pandas as pd
    ###################### Add/Modify the search space below ###########################
    params = {
        'n_estimators': list(np.linspace(50, 500, 5, dtype=int)) + list(np.linspace(500, 1500, 10, dtype=int)),
        'min_samples_split': list(np.linspace(0.1, 1, 5)) + list(np.linspace(2, 200, 10, dtype=int)) + list(
            np.linspace(200, 600, 5, dtype=int)),
        'max_depth': [None] + list(np.linspace(1, 15, 5, dtype=int)),
        'random_state': [42],
    }
    #####################################################################################
    # Initializing the random search with random forest model
    clf = RandomizedSearchCV(
        estimator=RandomForestClassifier(random_state=42),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='roc_auc',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models
    clf.fit(X_train, y_train)
    # Storing the metrics
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_gini = []
    test_gini = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = RandomForestClassifier(**df_cv['params'][i])
        model.fit(X_train, y_train)
        # Getiing gini score
        train_gini.append(gini_index(y_train, model.predict(X_train)))
        test_gini_score = gini_index(y_test, model.predict(X_test))
        test_gini.append(test_gini_score)
        # Make a model best when it has the highest gini score
        if test_gini_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_gini, test_gini), columns=['train_gini', 'test/oot_gini'])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values('test/oot_gini', ascending=False)

    if (output_df['train_gini'] > train_gini_threshold).any() and (
            output_df['test/oot_gini'] > oot_gini_threshold).any():
        print("Search script was able to find random forest models above {} train and {} test/oot_threshold".format(
            train_gini_threshold, oot_gini_threshold))
    else:
        print("No random forest models were found that surpasses the given threshold")

    return best_model, output_df, clf.best_estimator_, clf


def search_logistic_regression_classification(X_train, X_test, y_train, y_test, train_gini_threshold=0.7,
                                              oot_gini_threshold=0.7, n_iter=25, cv=5):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import RandomizedSearchCV
    import numpy as np
    import pandas as pd
    ###################### Add/Modify the search space below ###########################
    params = {'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
              'penalty': ['none', 'l2'],
              'C': list(np.geomspace(1e-5, 1e3, 10)),
              'fit_intercept': [True, False]
              }
    #####################################################################################
    # Initializing the random search object with parameter space and random forest model
    clf = RandomizedSearchCV(
        estimator=LogisticRegression(random_state=42),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='roc_auc',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models
    clf.fit(X_train, y_train)
    # Storing the metrics
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_gini = []
    test_gini = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = LogisticRegression(**df_cv['params'][i])
        model.fit(X_train, y_train)
        # Getiing gini score
        train_gini.append(gini_index(y_train, model.predict(X_train)))
        test_gini_score = gini_index(y_test, model.predict(X_test))
        test_gini.append(test_gini_score)
        # Make a model best when it has the highest gini score
        if test_gini_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_gini, test_gini), columns=['train_gini', 'test/oot_gini'])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values('test/oot_gini', ascending=False)

    if (output_df['train_gini'] > train_gini_threshold).any() and (
            output_df['test/oot_gini'] > oot_gini_threshold).any():
        print(
            "Search script was able to find logistic regression models above {} train and {} test/oot_threshold".format(
                train_gini_threshold, oot_gini_threshold))
    else:
        print("No logistic regression models were found that surpasses the given threshold")

    return best_model, output_df, clf.best_estimator_, clf
