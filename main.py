
# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return first and last names of employees working in Boston
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees AS e
    JOIN offices AS o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
    ORDER BY e.firstName, e.lastName;
""", conn)

# STEP 2
# Find offices that have zero employees
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode
    FROM offices AS o
    LEFT JOIN employees AS e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
""", conn)

# STEP 3
# Return all employees and their office city and state
df_employee = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees AS e
    LEFT JOIN offices AS o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName;
""", conn)

# STEP 4
# Find customers who have never placed an order
df_contacts = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers AS c
    LEFT JOIN orders AS ord
        ON c.customerNumber = ord.customerNumber
    WHERE ord.orderNumber IS NULL
    ORDER BY c.contactLastName;
""", conn)

# STEP 5
# Return customer contact details and payment information
df_payment = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM customers AS c
    JOIN payments AS p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6
# Find sales representatives whose customers have an average
# credit limit greater than 90,000
df_credit = pd.read_sql("""
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS numcustomers
    FROM employees AS e
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        e.employeeNumber,
        e.firstName,
        e.lastName
    HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
    ORDER BY numcustomers DESC;
""", conn)

# STEP 7
# Return product names, number of orders, and total units sold
df_product_sold = pd.read_sql("""
    SELECT
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Count distinct customers who purchased each product
df_total_customers = pd.read_sql("""
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT ord.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderdetails AS od
        ON p.productCode = od.productCode
    JOIN orders AS ord
        ON od.orderNumber = ord.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
# Count customers assigned to each office
df_customers = pd.read_sql("""
    SELECT
        COUNT(DISTINCT c.customerNumber) AS n_customers,
        o.officeCode,
        o.city
    FROM offices AS o
    LEFT JOIN employees AS e
        ON o.officeCode = e.officeCode
    LEFT JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode;
""", conn)

# STEP 10
# Find employees who sold products purchased by fewer than
# 20 distinct customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM employees AS e
    JOIN offices AS o
        ON e.officeCode = o.officeCode
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders AS ord
        ON c.customerNumber = ord.customerNumber
    JOIN orderdetails AS od
        ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails AS od2
        JOIN orders AS ord2
            ON od2.orderNumber = ord2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName;
""", conn)

conn.close()
