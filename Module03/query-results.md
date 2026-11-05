# Module 3 Query Results

## Database setup check

```text
customer     order_line     orders     product
```

## Row counts

```text
╭──────────┬──────────╮
│ 'orders' │ COUNT(*) │
╞══════════╪══════════╡
│ orders   │    60000 │
│ lines    │   240000 │
╰──────────┴──────────╯
```

Looking at the plan:
QUERY PLAN
|--SCAN ol
|--SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
|--SEARCH p USING INTEGER PRIMARY KEY (rowid=?)
|--USE TEMP B-TREE FOR GROUP BY
|--USE TEMP B-TREE FOR count(DISTINCT)
`--USE TEMP B-TREE FOR ORDER BY



The Report:
╭───────────┬───────────┬────────────╮
│   city    │ customers │  revenue   │
╞═══════════╪═══════════╪════════════╡
│ Bielefeld │       500 │ 11242176.0 │
│ Gütersloh │       500 │  8422344.0 │
│ Münster   │       500 │  5493504.0 │
│ Paderborn │       500 │  2815656.0 │
╰───────────┴───────────┴────────────╯


After running the python script, the result were:
normal   : [(1, 'Customer 1')]
injected : [(1, 'Customer 1'), (2, 'Customer 2'), (3, 'Customer 3')] ...
safe     : []