-- send everything from here into a file
.output Module01/shell-tour.txt
.tables
.schema reading
SELECT machine, max(vib) AS peak FROM reading GROUP BY machine;

-- the whole schema + data as SQL
.dump


.output stdout
.quit