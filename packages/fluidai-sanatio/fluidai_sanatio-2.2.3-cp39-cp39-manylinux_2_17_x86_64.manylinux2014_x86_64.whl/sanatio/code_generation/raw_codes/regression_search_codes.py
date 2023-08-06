def search_xgb_regression(X_train, X_test, y_train, y_test, train_r2_threshold=0.7, oot_r2_threshold=0.7, n_iter=25,
                          cv=5):
    from xgboost import XGBRegressor
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import r2_score
    import numpy as np
    import pandas as pd
    ###################### Add/Modify the search space below ###########################
    params = {
        'learning_rate': list(np.linspace(0.01, 0.1, 10)) + list(np.linspace(0.1, 0.5, 5)),
        'n_estimators': list(np.linspace(50, 500, 5, dtype=int)) + list(np.linspace(500, 1500, 10, dtype=int)),
        'subsample': list(np.linspace(0.5, 1, 5)) + [1],
        'min_child_weight': list(np.linspace(0, 1, 5)) + list(np.linspace(1, 200, 10)) + list(np.linspace(200, 600, 5)),
        'max_value_depth': [3, 4, 5],
        'scale_pos_weight': [1] + list(np.linspace(0.5, 2, 5)) + list(np.linspace(2, 20, 3)),
        'random_state': [42],
    }
    #####################################################################################
    # Initializing the random search with xgb model
    clf = RandomizedSearchCV(
        estimator=XGBRegressor(eval_metric="mae", use_label_encoder=False, seed=42),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='r2',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models over the parameter space defined above
    clf.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=0)
    # Storing the results in a dataframe
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_r2 = []
    test_r2 = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = XGBRegressor(**df_cv['params'][i])
        model.fit(X_train, y_train, early_stopping_rounds=10, eval_set=[(X_test, y_test)], verbose=0)
        # Getiing r2 score
        train_r2.append(r2_score(y_train, model.predict(X_train)))
        test_r2_score = r2_score(y_test, model.predict(X_test))
        test_r2.append(test_r2_score)
        # Make a model best when it has the highest r2 score
        if test_r2_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_r2, test_r2), columns=['train_r2', "test/oot_r2"])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values("test/oot_r2", ascending=False)

    if (output_df['train_r2'] > train_r2_threshold).any() and (output_df["test/oot_r2"] > oot_r2_threshold).any():
        print("Search script was able to find xgb models above {} train and {} test/oot_threshold".format(
            train_r2_threshold, oot_r2_threshold))
    else:
        print("No xgb models were found that surpasses the given threshold")

    return best_model, output_df, clf.best_estimator_, clf


def search_random_forest_regression(X_train, X_test, y_train, y_test, train_r2_threshold=0.7, oot_r2_threshold=0.7,
                                    n_iter=25, cv=5):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import r2_score
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
        estimator=RandomForestRegressor(random_state=42),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='r2',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models
    clf.fit(X_train, y_train)
    # Storing the metrics
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_r2 = []
    test_r2 = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = RandomForestRegressor(**df_cv['params'][i])
        model.fit(X_train, y_train)
        # Getiing r2 score
        train_r2.append(r2_score(y_train, model.predict(X_train)))
        test_r2_score = r2_score(y_test, model.predict(X_test))
        test_r2.append(test_r2_score)
        # Make a model best when it has the highest r2 score
        if test_r2_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_r2, test_r2), columns=['train_r2', "test/oot_r2"])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values("test/oot_r2", ascending=False)

    if (output_df['train_r2'] > train_r2_threshold).any() and (output_df["test/oot_r2"] > oot_r2_threshold).any():
        print("Search script was able to find random forest models above {} train and {} test/oot_threshold".format(
            train_r2_threshold, oot_r2_threshold))
    else:
        print("No random forest models were found that surpasses the given threshold")
    return best_model, output_df, clf.best_estimator_, clf


def search_linear_regression(X_train, X_test, y_train, y_test, train_r2_threshold=0.7, oot_r2_threshold=0.7, n_iter=25,
                             cv=5):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import r2_score
    import pandas as pd
    ###################### Add/Modify the search space below ###########################
    params = {
        'fit_intercept': [True, False],
        'normalize': [True, False]
    }
    #####################################################################################
    # Initializing the random search object with parameter space and random forest model
    clf = RandomizedSearchCV(
        estimator=LinearRegression(),
        param_distributions=params,
        random_state=42,
        n_iter=n_iter,
        scoring='r2',
        verbose=0,
        cv=cv,
        n_jobs=-1,
    )
    # Training the models
    clf.fit(X_train, y_train)
    # Storing the metrics
    df_cv = pd.DataFrame(clf.cv_results_)
    # Declaring variable needed for the loop
    train_r2 = []
    test_r2 = []
    best_model = None
    max_value = 0
    # Looping over the different models
    for i in range(len(df_cv)):
        # Training the model
        model = LinearRegression(**df_cv['params'][i])
        model.fit(X_train, y_train)
        # Getiing r2 score
        train_r2.append(r2_score(y_train, model.predict(X_train)))
        test_r2_score = r2_score(y_test, model.predict(X_test))
        test_r2.append(test_r2_score)
        # Make a model best when it has the highest r2 score
        if test_r2_score > max_value:
            best_model = model
    # Creating a dataframe
    output_df = pd.DataFrame(zip(train_r2, test_r2), columns=['train_r2', "test/oot_r2"])
    results_column = df_cv.columns.values
    output_df[results_column] = df_cv[results_column]
    output_df = output_df.sort_values("test/oot_r2", ascending=False)

    if (output_df['train_r2'] > train_r2_threshold).any() and (output_df["test/oot_r2"] > oot_r2_threshold).any():
        print("Search script was able to find linear regression models above {} train and {} test/oot_threshold".format(
            train_r2_threshold, oot_r2_threshold))
    else:
        print("No linear regression models were found that surpasses the given threshold")
    return best_model, output_df, clf.best_estimator_, clf
