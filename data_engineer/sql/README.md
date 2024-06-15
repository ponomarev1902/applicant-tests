# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items
```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
SELECT co.country_name, count(distinct *) CustomerCountDistinct
FROM
  Customer cu
  JOIN Countries co
  on cu.country_code = co.country_code
WHERE
  co.name in ('France', 'Italy')
GROUP BY
  co.country_name
```

### 2) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
SELECT
  cu.customer_name, sum(it.item_price) Revenue
FROM
  orders o
  LEFT JOIN customer cu
  on o.customer_id = cu.customer_id
  LEFT JOIN Items it
  on o.item_id = it.item_id
GROUP BY
  cu.customer_name
ORDER BY
  revenue desc
LIMIT 10
  
```

### 3) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
SELECT
  co.country_name, sum(item_price) RevenuePerCountry
FROM
  orders o
  LEFT JOIN customer cu
  on o.customer_id = cu.customer_id
  LEFT JOIN Items it
  on o.item_id = it.item_id
  FULL OUTER JOIN countries co
  on cu.country_code = co.country_code
GROUP BY
  c.country_name
```

### 4) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
SELECT DISTINCT ON(customer_id) customer_id, customer_name, item_name MostExpensiveItemName
FROM (
  SELECT
    cu.customer_id, cu.customer_name, it.item_name, it.item_price,
    max(it.item_price) OVER(PARTITION BY cu.customer_id) max_price
  FROM
    orders o
    LEFT JOIN customer cu
    on o.customer_id = cu.customer_id
    LEFT JOIN Items it
    on o.item_id = it.item_id
)
WHERE
  item_price = max_price
```

### 5) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
-- result here
```

### 6) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
SELECT DISTINCT ON(date_time, customer_id, item_id)
FROM
 (
  SELECT
    *
    , count(*) OVER(PARTITION BY date_time, customer_id, item_id) dublicates_count
  FROM
    orders
)
WHERE
  dublicates_count > 1;
```

### 7) Найти "важных" покупателей

Создать запрос, который найдет всех "важных" покупателей,
т.е. тех, кто совершил наибольшее количество покупок после своего первого заказа.

| **Customer\_id** | **Total Orders Count** |
| --------------------- |-------------------------------|
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |

```sql
-- result here
```

### 8) Найти покупателей с "ростом" за последний месяц

Написать запрос, который найдет всех клиентов,
у которых суммарная выручка за последний месяц
превышает среднюю выручку за все месяцы.

| **Customer\_id** | **Total Revenue** |
| --------------------- |-------------------|
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
WITH SELECT as other_monthes (
SELECT
  *
  , mean(it.item_price) mean_revenue
FROM
  orders o
  LEFT JOIN customer cu
  on o.customer_id = cu.customer_id
  LEFT JOIN Items it
  on o.item_id = it.item_id
  FULL OUTER JOIN countries co
  on cu.country_code = co.country_code
WHERE
  date_trunc('month', o.date_time) < date_trunc('month', current_date - interval '1 month') -- Покупки за предыдущие месяца
GROUP BY
  cu.customer_id
),
last_month as (
SELECT
  *
  , sum(it.item_price) total_revenue
FROM
  orders o
  LEFT JOIN customer cu
  on o.customer_id = cu.customer_id
  LEFT JOIN Items it
  on o.item_id = it.item_id
  FULL OUTER JOIN countries co
  on cu.country_code = co.country_code
WHERE
  date_trunc('month', o.date_time) = date_trunc('month', current_date - interval '1 month') -- Покупки за последний месяц
GROUP BY
  cu.customer_id
) SELECT
    Customer_id, total_revenue
  FROM
    last_month lm
    JOIN other_montes om
    on lm.customer_id = om.customer_id
WHERE
  lm.total_revenue > om.mean_revenue
  
```
