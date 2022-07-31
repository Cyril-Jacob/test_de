-- Tested on BigQuery with Google Standard SQL dialect

-- Convert STRING to DECIMAL type
CREATE TEMP FUNCTION
  convert_str_to_dec(str STRING)
  RETURNS DECIMAL AS ( CAST(REPLACE(str,',','.') AS DECIMAL) );

-- Convert STRING to DATE type
CREATE TEMP FUNCTION
  convert_str_to_date(str STRING)
  RETURNS DATE AS ( PARSE_DATE('%d/%m/%y', str) );

-- Convert DECIMAL to STRING type
CREATE TEMP FUNCTION
  convert_dec_to_str(dec DECIMAL)
  RETURNS STRING AS ( REPLACE(CAST(dec AS STRING), '.',',') );

-- Compute sale order: (product price) * (product quantity)
CREATE TEMP FUNCTION
  compute_sale_order(price STRING, qty STRING)
  RETURNS DECIMAL AS (convert_str_to_dec(price) * CAST(qty AS DECIMAL) );

-- Join transaction and product nomenclature on product id
-- Filter out other products than MEUBLE and DECO
-- Aggregate on the period  
WITH
  sales_per_client_and_product AS (
  SELECT
    client_id,
    product_type,
    SUM(compute_sale_order(prod_price, prod_qty)) AS total_sale
  FROM
    `keen-vigil-357522.test.transaction` AS transac
  JOIN
    `keen-vigil-357522.test.product_nomenclature` AS nomen
  ON
    transac.prod_id = nomen.product_id
  WHERE
    (product_type = 'MEUBLE'
      OR product_type = 'DECO')
    AND "2019-01-01" <= convert_str_to_date(date)
    AND "2019-12-31" >= convert_str_to_date(date)
  GROUP BY
    client_id,
    product_type ),
  
  -- pivot table on product_type MEUBLE and DECO
  sales_per_client AS (
  SELECT
    *
  FROM
    sales_per_client_and_product 
  PIVOT (SUM(total_sale) 
  FOR product_type IN ('MEUBLE' AS ventes_meuble,'DECO' AS ventes_deco))
  ORDER BY
    client_id DESC )

-- replace NULL values per 0 and display product sales per client as STRING
SELECT
  client_id,
  convert_dec_to_str(IFNULL(ventes_meuble, 0)) AS ventes_meuble,
  convert_dec_to_str(IFNULL(ventes_deco, 0)) AS ventes_meuble
FROM
  sales_per_client