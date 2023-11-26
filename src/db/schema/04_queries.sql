"""
Join two tables so that the product table contains human-readable city name
"""
SELECT cities.id, cities.name, total_counts_per_city.unit_type, total_counts_per_city.total_count
FROM cities
JOIN total_counts_per_city ON cities.id = total_counts_per_city.city_id;
