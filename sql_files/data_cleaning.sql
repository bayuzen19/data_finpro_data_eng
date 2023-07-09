COPY (
    select * from data_customer
    where effective_start_date is not null
) TO '/var/lib/postgres/data/data_preprepation.csv' WITH (FORMAT CSV, HEADER);