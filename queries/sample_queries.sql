--- 1- Names of law firms which have not yet brought any cases:
 
SELECT r.group_id, l.firm_name
FROM representations r
RIGHT OUTER JOIN law_firms l
ON r.law_firm_name = l.firm_name
WHERE group_id is NULL;
 
--- 2 - Count of negative determinations by country:
 
SELECT c.country_name, COUNT(i.investigation_number) as inv_count
FROM investigations i
    LEFT JOIN determinations d
    ON i.investigation_number = d.investigation_number
    LEFT JOIN country c
    ON i.country_code = c.country_code
WHERE d.determination = 'Negative'
GROUP BY c.country_name
ORDER BY c.country_name DESC ;
 
--- 3 - Ranking of most successful law firms at getting an affirmative determination in the Final phase:
 
SELECT RANK() OVER(ORDER BY COUNT(d.determination)) AS rank, r.law_firm_name, COUNT(d.determination) as affirmative_determinations
    FROM representations r
    JOIN investigations i
    ON i.group_id = r.group_id
    JOIN determinations d
    ON d.investigation_number = i.investigation_number
WHERE d.determination = 'Affirmative'
GROUP BY (r.law_firm_name);
 
--- 4- Dense ranking of ITC staff members by number of cases worked with certain title :
 
SELECT DENSE_RANK() OVER(ORDER BY COUNT(a.group_id)) AS rank, s.name, s. title, COUNT(a.group_id) as cases_worked_in_role
    FROM staff_assigned a
    JOIN itc_staff s
    ON a.staff_id = s.id
GROUP BY (s.name, s.title);
 
--- 5 - Ranking of countries of origin by number of cases but only with the products Glycine and Mattresses

SELECT p.product_id, RANK() OVER(ORDER BY COUNT(c.country)) AS rank, s., s. title, COUNT(a.Investigation_number) as cases_per country
    FROM Investigations i
    LEFT JOIN country c
    ON i.country_code = c.country_code
    LEFT JOIN products p
    ON i.product_id = p.product_id
GROUP BY (c.country)
WHERE product_name IN (‘Mattresses’, ‘Glycine ‘);
 
--- 6 - Finding the top 3 product names that have the most investigations against countries in Europe
 
SELECT p.product_name 
FROM (
SELECT p.product_id, p.product_name c.country_code, COUNT(Investigation_number) as Cnt
FROM investigations i
LEFT JOIN products p
    ON i.product_id = p.product_id
LEFT JOIN country c
    ON i.country_code = c.country_code
GROUP BY p.product_id
WHERE c.region = ‘Europe’
ORDER BY Cnt DESC
LIMIT 3
) tbl
 
 
--- 7 - Finding all of product_ids and and groups_ids that have cooperated At least three times
 
SELECT product_id, group_id
FROM 
(
SELECT product_id, group_id, COUNT(*) as cnt
FROM Investigations
GROUP BY product_id, group_id
) tbl
WHERE cnt >= 3
 
--- 8 - Finding Final determinations that were made on Friday
 
SELECT phase, day_name 
    FROM determinations d
    JOIN date_dim a
    ON d.hearing_date = a.date
WHERE d.day_name = ‘Friday’ AND a.phase = ‘Final’
 
 
--- 9 - Finding cases against aluminum products that were brought in 2021

SELECT p.product_name 
FROM (
SELECT p.product_id, p.product_name c.country_code, hearing_date, date
FROM investigations i
LEFT JOIN products p
    ON i.product_id = p.product_id
LEFT JOIN determinations d
    ON i.investigation_number= d.investigation_number
LEFT JOIN date_dim da
ON d.hearing_date= da.date
WHERE da.year_value= 2021 AND product_name = ‘Aluminum’)
 
--- 10 - Counting cases that went Negative or were Terminated 

SELECT COUNT(i.investigation_number) as num_of_cases
FROM investigations i
    LEFT JOIN determinations d
    ON i.investigation_number = d.investigation_number
    LEFT JOIN date_dim da
    ON d.hearing_date = da.date
WHERE d.determination = 'Negative' OR d.determination = ‘Terminated’
