--Name of law firm which has not brought any cases

SELECT l.firm_name
FROM law_firms l
  LEFT OUTER JOIN representations r 
  ON l.firm_name = r.law_firm_name
WHERE l.law_firm_name IS NULL;

--count of negative determinations by country

SELECT c.country_name, COUNT(i.investigation_number) as inv_count
FROM investigations i
	LEFT JOIN determinations d
	ON i.investigation_number = d.investigation_number
	LEFT JOIN country c
	ON i.country_code = c.country_code
WHERE d.determination IS "Negative"
ORDER BY country_name DESC ;

--most successful law firms at getting affirmatives in the Final

SELECT RANK() OVER(ORDER BY COUNT(d.determination)) AS rank, r.firm_name, COUNT(d.determination) as affirmative_determinations
	FROM representations r
	JOIN investigations i
	ON i.group_id = r.group_id
	JOIN determinations d
	ON d.investigation_number = i.investigation_number
WHERE d.determination = "Affirmative";