CREATE TABLE [dp700_practice_scd].[dim_product_scd2] (
    [surrogate_key]     INT             NULL,
    [product_id]        INT             NULL,
    [product_name]      VARCHAR (100)   NULL,
    [price]             DECIMAL (10, 2) NULL,
    [record_start_date] DATE            NULL,
    [record_end_date]   DATE            NULL,
    [is_current]        BIT             NULL
);


GO