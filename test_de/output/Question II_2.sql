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

-- Since Transaction table consists only of STRING type, we need to properly
-- convert them in order to determine the total amount of sales per day betweent 
-- January 1st, 2019 and December 31, 20219 included
SELECT
  date,
  convert_dec_to_str(SUM(compute_sale_order(prod_price, prod_qty))) AS total_sale
FROM
  `keen-vigil-357522.test.transaction`
WHERE
  "2019-01-01" <= convert_str_to_date(date)
  AND "2019-12-31" >= convert_str_to_date(date)
GROUP BY
  date
ORDER BY
  date ASC