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

CREATE TABLE units_per_city (
  id SERIAL PRIMARY KEY,
  city_id INTEGER REFERENCES cities(id),
  unit_type unit_types NOT NULL,
  transaction_type transaction_types NOT NULL,
  address varchar(255) NOT NULL,
  square_meters INTEGER NOT NULL,
  floor INTEGER,
  rooms INTEGER,
  url varchar(255) NOT NULL,
  offer_heading varchar(255) NOT NULL,
  is_private_offer BOOLEAN NOT NULL,
  currency currency_types NOT NULL,
  is_stale BOOLEAN DEFAULT FALSE,
  bait_price INTEGER NOT NULL,
  additional_price INTEGER,
  security_deposit INTEGER,
  supposed_final_price INTEGER,
  source_created_at TIMESTAMP,
  source_updated_at TIMESTAMP
  scraped_and_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
)


GRANT SELECT ON cities TO my_user;

GRANT USAGE, SELECT ON SEQUENCE total_counts_per_city_id_seq TO my_user;
GRANT INSERT ON TABLE total_counts_per_city TO my_user;
