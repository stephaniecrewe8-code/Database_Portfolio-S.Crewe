.timer on

-- Defect 1: orphan maintenance jobs (machine_name not in machine)
SELECT m.job_id, m.machine_name
FROM maint_job m
LEFT JOIN machine x ON m.machine_name = x.machine_name
WHERE x.machine_name IS NULL;


job_id  machine_name
------  ------------
     3  cnc-05

A maintenance job could be recorded for a machine that does not exist, making its history unreliable.

-- Defect 2: duplicate natural keys in part
SELECT part_no, COUNT(*) AS copies
FROM part GROUP BY part_no HAVING COUNT(*) > 1;


part_no  copies
-------  ------
P-1003        2

A job could list a part that is not in the parts catalog, causing inventory and cost records to be wrong.

-- Defect 3: unit_price stored as text — a numeric comparison fails silently
SELECT part_no, unit_price FROM part WHERE unit_price < '15';   -- 'text ordering', not money!


part_no  unit_price
-------  ----------
P-1001   12.50

The same maintenance work could be counted twice, overstating labor, parts usage, or maintenance costs.

-- Defect 4: installed dates that are not dates
SELECT machine_name, installed FROM machine
WHERE installed NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]';


machine_name  installed
------------  ---------
RANDOM-NAME   unknown

An incomplete job record could make it impossible to tell what work was performed or when.

-- Defect 5: the m:n list only "joins" when it holds exactly one part
SELECT j.job_id, p.description
FROM maint_job j
JOIN part p ON p.part_no = j.parts_used;   -- the list is not a key
-- Watch what happens: job 2 ('P-1003') and job 3 ('P-1001') match, but job 1
-- ('P-1001,P-1002') silently disappears. A naive join on the list loses every
-- multi-part job — and reports success while doing it. That silence is the defect.


job_id     description
------  -----------------
     2  Coolant filter
     2  Coolant filter
     3  Ball bearing 6203

Incorrect values could distort maintenance timelines, inventory totals, or reports.     