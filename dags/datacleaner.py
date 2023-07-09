def data_preparation_modelling():
    import pandas as pd
    df = pd.read_csv("~/store_files_airflow/data_preprepation.csv")
    df = df.dropna(subset=["effective_start_date"])
    df["with_phone_service"] = df["with_phone_service"].astype(int)
    df["current_month_churn"] = df["current_month_churn"].astype(int)
    df = df.groupby(["account_no"]).agg({
    "tenure":"max",
    "contract_month":"max",
    "bill_amount":"sum",
    "complaint_cnt":"sum",
    "with_phone_service":"max",
    "current_month_churn":"sum"
    }).reset_index()

    df.to_csv("~/store_files_airflow/data_for_modelling.csv",index=False)
    
