def modelling():
    import pandas as pd 
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (accuracy_score,
                                recall_score,
                                precision_score,
                                f1_score,
                                roc_auc_score)
    from sklearn.model_selection import train_test_split

    df = pd.read_csv("~/store_files_airflow/data_for_modelling.csv")
    df = df.set_index("account_no")
    
    X = df.drop("current_month_churn",axis=1)
    y = df["current_month_churn"]
    
    X_train,X_test,y_train,y_test = train_test_split(
        X,
        y,
        stratify=y,
        random_state=42,
        test_size=0.3,
        train_size=0.7
    )

    lr = LogisticRegression(random_state=42)
    xgb = XGBClassifier(random_state=42,max_depth=5)
    rf = RandomForestClassifier(random_state=42,max_depth=5)

    lr.fit(X_train,y_train)
    xgb.fit(X_train,y_train)
    rf.fit(X_train,y_train)

    acc_train = []
    acc_test = []
    pre_train = []
    pre_test = []
    rec_train = []
    rec_test = []
    f1_train = []
    f1_test = []
    roc_train = []
    roc_test = []
    model = []
    df_eval = pd.DataFrame(columns=["acc_train", "acc_test", "pre_train", "pre_test", "rec_train", "rec_test",
                                    "f1_train", "f1_test", "roc_train", "roc_test", "model"])

    for ml in [lr, xgb, rf]:
        y_pred_tr = ml.predict(X_train)
        y_pred_test = ml.predict(X_test)
        y_train_proba = ml.predict_proba(X_train)[:, 1]
        y_test_proba = ml.predict_proba(X_test)[:, 1]

        acc_train.append(accuracy_score(y_train, y_pred_tr))
        acc_test.append(accuracy_score(y_test, y_pred_test))

        pre_train.append(precision_score(y_train, y_pred_tr))
        pre_test.append(precision_score(y_test, y_pred_test))

        rec_train.append(recall_score(y_train, y_pred_tr))
        rec_test.append(recall_score(y_test, y_pred_test))

        f1_train.append(f1_score(y_train, y_pred_tr))
        f1_test.append(f1_score(y_test, y_pred_test))

        roc_train.append(roc_auc_score(y_train, y_train_proba))
        roc_test.append(roc_auc_score(y_test, y_test_proba))

    df_eval["acc_train"] = acc_train
    df_eval["acc_test"] = acc_test
    df_eval["pre_train"] = pre_train
    df_eval["pre_test"] = pre_test
    df_eval["rec_train"] = rec_train
    df_eval["rec_test"] = rec_test
    df_eval["f1_train"] = f1_train
    df_eval["f1_test"] = f1_test
    df_eval["roc_train"] = roc_train
    df_eval["roc_test"] = roc_test
    df_eval['model'] = [ml.__class__.__name__ for ml in [lr, xgb, rf]]

    df_eval.to_csv("~/store_files_airflow/data_evaluation_metrics.csv")

    # Get feature importances
    importances = xgb.feature_importances_

    # Create a DataFrame with feature names and importances
    feature_importances = pd.DataFrame({'Feature': X_train.columns, 'Importance': importances})

    # Sort the DataFrame by importance in descending order
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    feature_importances.to_csv("~/store_files_airflow/feature_importance.csv",index=False)
    
