# Module 3 Reflection

I learned that getting SQL to run does not prove that it answers the question correctly. I checked the report query by reviewing its joins, date filter, customer count, and query plan.
The query plan helped me see whether SQLite scanned rows or used an index. I also learned that adding an index does not guarantee a query will become faster, so I recorded the plans and timings I measured.The SQL injection exercise showed me why user input should be passed as a bound parameter instead of being joined into a SQL string.
