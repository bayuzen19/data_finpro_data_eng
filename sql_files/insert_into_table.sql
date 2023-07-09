-- LOAD DATA INFILE '/var/lib/mysql-files/data_customer_clean.csv' INTO TABLE data_customer FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
COPY data_customer FROM '/var/lib/postgres/data/customer_churn_data.csv' DELIMITER AS ',' CSV HEADER;
SELECT * FROM data_customer LIMIT 5;