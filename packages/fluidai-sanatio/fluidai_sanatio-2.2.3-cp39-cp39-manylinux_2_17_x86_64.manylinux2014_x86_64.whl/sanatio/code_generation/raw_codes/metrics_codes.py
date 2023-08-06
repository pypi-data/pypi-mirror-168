def gini_index(actual, predicted_probability):
    # Calcualtin gini index
    from sklearn import metrics
    fpr, tpr, thresholds = metrics.roc_curve(actual, predicted_probability)
    area_under_curve = metrics.auc(fpr, tpr)
    gini_index = 2 * area_under_curve - 1

    return gini_index
