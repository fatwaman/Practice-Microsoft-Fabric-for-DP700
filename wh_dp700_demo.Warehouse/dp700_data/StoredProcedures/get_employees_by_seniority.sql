CREATE PROCEDURE dp700_data.get_employees_by_seniority
    @seniority_level VARCHAR(20),
    @department_id INT = NULL
AS
BEGIN
    SELECT
        employee_id,
        name,
        department_id,
        hire_date,
        salary,
        years_employed,
        seniority_level
    FROM dp700_data.vw_employees
    WHERE seniority_level = @seniority_level
        AND (@department_id IS NULL OR department_id = @department_id);
END;

GO