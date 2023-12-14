CREATE TABLE cities (
  id SERIAL PRIMARY KEY,
  name varchar(80) UNIQUE NOT NULL
);


CREATE TABLE total_counts_per_city (
  id SERIAL PRIMARY KEY,
  city_id INTEGER REFERENCES cities(id),
  unit_type unit_types NOT NULL,
  total_count INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  transaction_type transaction_types NOT NULL
);


GRANT SELECT ON cities TO my_user;

GRANT USAGE, SELECT ON SEQUENCE total_counts_per_city_id_seq TO my_user;
GRANT INSERT ON TABLE total_counts_per_city TO my_user;
