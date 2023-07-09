DROP TABLE IF EXISTS data_customer;

CREATE TABLE IF NOT EXISTS data_customer (
  month DATE NULL,
  account_no TEXT NULL,
  tenure INT NULL,
  effective_start_date TEXT NULL,
  effective_end_date TEXT NULL,
  contract_month FLOAT NULL,
  bill_amount FLOAT NULL,
  bandwidth TEXT NULL,
  term_reason_code TEXT NULL,
  term_reason_description TEXT NULL,
  complaint_cnt INT NULL,
  with_phone_service TEXT NULL,
  current_month_churn TEXT NULL,
  is_new_customer_account INT NULL
);
