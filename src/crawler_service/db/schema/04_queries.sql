"""
Join two tables so that the product table contains human-readable city name
"""
SELECT cities.id, cities.name, total_counts_per_city.unit_type, total_counts_per_city.transaction_type, total_counts_per_city.total_count
FROM cities
JOIN total_counts_per_city ON cities.id = total_counts_per_city.city_id;


"""
Get the total count of apartments for rent in city with id 10 (Poznań)
"""
select * from total_counts_per_city where city_id = 10 AND unit_type = 'apartment' AND transaction_type = 'rent';
