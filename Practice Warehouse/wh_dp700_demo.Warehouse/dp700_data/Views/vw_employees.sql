CREATE VIEW dp700_data.vw_employees AS
SELECT
    employee_id,
    name,
    department_id,
    hire_date,
    salary,
    DATEDIFF(YEAR, hire_date, GETDATE()) AS years_employed,
    CASE
        WHEN DATEDIFF(YEAR, hire_date, GETDATE()) >= 8 THEN 'Senior'
        WHEN DATEDIFF(YEAR, hire_date, GETDATE()) >= 5 THEN 'Mid-Level'
        ELSE 'Junior'
    END AS seniority_level
FROM dp700_data.employees;

GO