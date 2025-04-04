SELECT * FROM users	sample
SELECT name, age FROM users WHERE age > 18	sample
SELECT COUNT(*) FROM orders	sample
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name HAVING COUNT(o.id) > 0	sample
SELECT u.name, o.total, RANK() OVER (ORDER BY o.total DESC) as spending_rank FROM users u JOIN orders o ON u.id = o.user_id	sample
SELECT CASE WHEN age < 18 THEN 'Under 18' WHEN age BETWEEN 18 AND 30 THEN '18-30' ELSE 'Over 30' END as age_group, COUNT(*) as count FROM users GROUP BY CASE WHEN age < 18 THEN 'Under 18' WHEN age BETWEEN 18 AND 30 THEN '18-30' ELSE 'Over 30' END	sample
