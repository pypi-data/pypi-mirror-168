def find_columns_type(dataframe, unique_no_threshold=None):
    '''
    This function is used to find whether a column is categorical or continuous depending upon the number of unique entries threshold passed or the type of data

    :param dataframe: DataFrame
    :param unique_no_threshold: int - Number of unique values to be considered for a column to be a categorical or numerical
    :return: tuple - Tuple of categorical column list and numerical column list
    '''
    import numpy as np

    numerical_columns = []
    categorical_columns = []
    if unique_no_threshold is None:
        # Checking if dataframetype is not object type
        categorical_columns = list(dataframe.dtypes[dataframe.dtypes == 'object'].index)
        numerical_columns = list(dataframe.dtypes[dataframe.dtypes != 'object'].index)
    else:
        for feature in dataframe.columns:
            if dataframe[feature].unique().shape[0] <= unique_no_threshold:
                categorical_columns.append(feature)
            else:
                numerical_columns.append(feature)
    return categorical_columns, numerical_columns


def numericals_summary(dataframe, numerical_columns):
    """
    A function to generate a summary dataframe with the numerical columns available in the dataframe given

    :param dataframe: DataFrame
    :param numerical_columns: list - names of numerical_columns
    :return: DataFrame - Summary
    """
    import pandas as pd

    dataframe = dataframe.copy()

    # Slicing non numerical columns
    dataframe = dataframe[numerical_columns]
    temp = dataframe.describe().T.reset_index().rename(columns={'index': 'column'})

    # Getting missing and uniue dataframe for each column
    missing = (100 * (dataframe.isna().sum() / dataframe.shape[0])).reset_index().rename(
        columns={'index': 'column', 0: 'missing_%'})
    output_df = pd.merge(temp, missing, on='column')

    nuniques = dataframe.apply(lambda x: x.nunique()).reset_index().rename(columns={'index': 'column', 0: 'nuniques'})
    output_df = pd.merge(output_df, nuniques, on='column')

    return output_df.round(3)


def categoricals_summary(dataframe, categorical_columns):
    """
    A function to generate a summary dataframe with the categorical columns available in the dataframe given

    :param dataframe: DataFrame
    :param categorical_columns: list - Names of categorical columns in dataframe
    :return: DataFrame- Summary
    """
    import pandas as pd

    dataframe = dataframe.copy()
    dataframe = dataframe[categorical_columns]

    # check nuniques
    temp = dataframe.apply(lambda x: x.nunique()).reset_index().rename(columns={'index': 'column', 0: 'nuniques'})

    # check count
    counts = dataframe.count().reset_index().rename(columns={'index': 'column', 0: 'count'})
    output_df = pd.merge(temp, counts, on='column')

    # check missing dataframe %
    missing = (100 * (dataframe.isna().sum() / dataframe.shape[0])).reset_index().rename(
        columns={'index': 'column', 0: 'missing_%'})
    output_df = pd.merge(output_df, missing, on='column')

    return output_df.round(3)


def skew_kurtosis_summary(dataframe, numerical_columns):
    """
    A function to generate the skew and kurtosis of numerical columns in a dataframe 
    
    :param dataframe: DataFrame
    :param numerical_columns: list - Names of numerical columns in dataframe
    :return: DataFrame- Summary
    """
    import pandas as pd

    temp = dataframe.copy()

    # skew and kurtosis calculation goes here
    skew = temp[numerical_columns].skew(axis=0, skipna=True).reset_index().rename(
        columns={'index': 'column', 0: 'Skew'})
    kurtosis = temp[numerical_columns].kurtosis(axis=0, skipna=True).reset_index().rename(
        columns={'index': 'column', 0: 'Kurtosis'})

    output_df = pd.merge(skew, kurtosis, on='column').sort_values(by=['Skew', 'Kurtosis'], ascending=[False, False])
    return output_df.round(3)


def pearson_correlation_filter(dataframe, columns, pearson_threshold=0.8):
    """
    This function is to generate the pearson correlated columns count summary and a filtered dataframe that has columns with correlation less than the threshold passed

    :param dataframe: DataFrame
    :param columns: list - Names of columns that you need to filter over using pearson
    :param pearson_threshold: float - optional

    :return: tuple - (correlation_count, filtered_dataframe)
    """
    other_columns = list(set(dataframe.columns.values.tolist()) - set(columns))
    temp = dataframe[columns].copy()

    # get correlation between columns
    correlation_matrix = temp.corr()

    # any column having correlation with others will be counted and removed
    correlation_count = ((correlation_matrix > pearson_threshold).sum() - 1).reset_index().rename(
        columns={'index': 'column', 0: 'count_corr_cols'})

    # remove columns with higher correlation
    filtered_dataframe = temp.drop(columns=correlation_count[correlation_count.count_corr_cols > 0].column.tolist())
    filtered_dataframe[other_columns] = dataframe[other_columns]

    return correlation_count, filtered_dataframe.round(3)

def chi_square_filter(dataframe, columns, chi_square_threshold=0.8):
    """
    This function is to generate the chi square correlated columns count summary and a filtered dataframe that had correlation less than the threshold passed

    :param dataframe: DataFrame
    :param columns: list - Name of columns that you need to filter over using chi square
    :param chi_square_threshold: float - optional

    :return: tuple - (correlation_count, filtered_dataframe)
    """
    from scipy.stats import chi2_contingency
    import pandas as pd

    other_columns = list(set(dataframe.columns.values.tolist()) - set(columns))
    temp = dataframe[columns].copy()
    categorical_columns = temp.columns.tolist()

    df_matrix = pd.DataFrame(index=categorical_columns, columns=categorical_columns)

    # Looping over categorical columns to create a relation matrix
    for col1 in categorical_columns:
        for col2 in categorical_columns:
            p_value = chi2_contingency(pd.crosstab(temp[col1], temp[col2]))[1]
            df_matrix[col1][col2] = p_value

    correlation_matrix = df_matrix
    # any column having correlation with others will be counted and removed
    correlation_count = ((correlation_matrix > chi_square_threshold).sum() - 1).reset_index().rename(
        columns={'index': 'column', 0: 'count_corr_cols'})

    # remove columns with higher correlation
    filtered_dataframe = temp.drop(columns=correlation_count[correlation_count.count_corr_cols > 0].column.tolist())
    filtered_dataframe[other_columns] = dataframe[other_columns]

    return correlation_count, filtered_dataframe

def p_val_filter(dataframe, target, columns, p_threshold=0.5):
    """
    This function is used to get a filtered dataframe and a pval summary that is based on the p value threshold passed

    :param dataframe: DataFrame
    :param target: DataSeries - actual truth value
    :param columns: list - Name of the columns that you need to filter over using pval

    :return: tuple- (p_val_summary, filtered_dataframe)
    """
    from sklearn.feature_selection import f_regression
    import pandas as pd

    other_columns = list(set(dataframe.columns.values.tolist()) - set(columns))

    X, y = dataframe[columns].copy(), target.copy()

    F, p_value = f_regression(X, y)

    predictor_columns_list = X.columns.to_list()

    # get the F score of each predictor in a dictionary format
    f_dict = dict(zip(predictor_columns_list, list(F)))
    f_scr_df = pd.DataFrame({'Variables': list(f_dict.keys()), 'F-score': list(f_dict.values())})

    # get the p_value of each predictor in a dictionary format
    p_dict = dict(zip(predictor_columns_list, list(p_value)))
    p_val_df = pd.DataFrame({'Variables': list(p_dict.keys()), 'P-values': list(p_dict.values())})

    p_val_summary = pd.merge(f_scr_df, p_val_df, on='Variables')

    p_val_summary['Hypothesis'] = (p_val_summary['P-values'] > p_threshold).replace(
        {True: 'Fail to Reject Null Hypothesis', False: 'Rejects Null Hypothesis'})

    filtered_dataframe = X[p_val_summary[p_val_summary['Hypothesis'] == 'Rejects Null Hypothesis'].Variables.tolist()]
    filtered_dataframe[other_columns] = dataframe[other_columns]

    return p_val_summary, filtered_dataframe

def vif_filter(dataframe, columns, vif_threshold=5):
    """
    This function generates the vif values of the filtered dataframe and returns the filtered dataframe based on the threshold.

    :param dataframe: DataFrame
    :param vif_threshold: int optional
    :return: tuple - (vif_value, filtered_dataframe)
    """
    import pandas as pd
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    def calculate_vif(data, threshold):
        temp = data.copy()

        frame_cols = temp.columns.tolist()

        # performing vif
        vif = {str(j): variance_inflation_factor(temp.values, i) for i, j in enumerate(frame_cols)}

        # get max vif
        max_vif = max(vif, key=lambda x: vif[x])

        # if the max vif is less than 5, stop iteration
        if vif[max_vif] <= threshold:
            return False

        # else keep dropping columns
        else:
            return max_vif

    other_columns = list(set(dataframe.columns.values.tolist()) - set(columns))
    temp = dataframe[columns].copy()

    # iterative application of vif to until the max vif is less than threshold
    max_vif = calculate_vif(temp, vif_threshold)
    while max_vif:
        temp.drop(columns=[max_vif], inplace=True, axis=1)
        max_vif = calculate_vif(temp, vif_threshold)

    # construct the final vif frame and return with temp
    frame_cols = temp.columns.tolist()
    vif = [variance_inflation_factor(temp.values, i) for i in range(len(frame_cols))]
    vif = pd.DataFrame({'column': frame_cols, 'vif': vif})

    vif.sort_values('vif', ascending=False, inplace=True)
    filtered_dataframe = temp
    filtered_dataframe[other_columns] = dataframe[other_columns]

    return vif, filtered_dataframe


def standardize_encoder(dataframe, columns_to_encode):
    """
    This function generates a standardized encoding only on the columns passed and returns the entire dataframe

    :param dataframe: DataFrame
    :param columns_to_encode: List - scalar columns that should be standard encoded

    :return: filtered_dataframe - DataFrame
    """
    from sklearn.preprocessing import StandardScaler
    import numpy as np

    # Converting to list if there is a single column
    if type(columns_to_encode) != list:
        columns_to_encode = [columns_to_encode]

    # Fitting the encoder
    scaler_object = StandardScaler().fit(dataframe[columns_to_encode].values)
    filtered_dataframe = dataframe.copy()

    # Applying encoding
    filtered_dataframe[columns_to_encode] = np.nan_to_num(
        scaler_object.transform(filtered_dataframe[columns_to_encode].values))

    return filtered_dataframe


def onehot_encoder(dataframe, columns_to_encode):
    """
    This function generates a one-hot encoding only on the columns passed and returns the entire dataframe

    :param dataframe: DataFrame
    :param columns_to_encode: List - scalar columns that should be standard encoded

    :return: filtered_dataframe
    """
    from sklearn.preprocessing import OneHotEncoder

    # Converting to list if there is a single column
    if type(columns_to_encode) != list:
        columns_to_encode = [columns_to_encode]

    # Fitting the encoder
    scaler_object = OneHotEncoder(handle_unknown='ignore', sparse=False).fit(dataframe[columns_to_encode].values)
    filtered_dataframe = dataframe.copy()

    # Applying encoding
    new_columns = scaler_object.get_feature_names(columns_to_encode)
    filtered_dataframe[new_columns] = scaler_object.transform(filtered_dataframe[columns_to_encode].values)
    filtered_dataframe.drop(columns=columns_to_encode, inplace=True)

    return filtered_dataframe


def robust_encoder(dataframe, columns_to_encode):
    """
    This function generates a robust scaling encoding only on the columns passed and returns the entire dataframe

    :param dataframe: DataFrame
    :param columns_to_encode: List - scalar columns that should be standard encoded

    :return: filtered_dataframe
    """
    from sklearn.preprocessing import RobustScaler
    import numpy as np

    # Converting to list if there is a single column
    if type(columns_to_encode) != list:
        columns_to_encode = [columns_to_encode]

    # Fitting the encoder
    scaler_object = RobustScaler().fit(dataframe[columns_to_encode].values)
    filtered_dataframe = dataframe.copy()

    # Applying encoding
    filtered_dataframe[columns_to_encode] = np.nan_to_num(
        scaler_object.transform(filtered_dataframe[columns_to_encode].values))

    return filtered_dataframe
