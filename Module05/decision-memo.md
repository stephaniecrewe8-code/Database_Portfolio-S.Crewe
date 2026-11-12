
# Recommendation to Yasmin Kaya

For the measured workload, keep the operational schema in **3NF** and do not use the indexed denormalized report table as the default dashboard path. The normalized query returned the same 350 grouped rows in a median **121.631 ms**; the report-table query with `ix_report_machine` took **197.303 ms**. Dropping the index and recompiling the plan brought the report-table median to **118.366 ms**, only slightly faster than the normalized query in this run. The site's update changed **1** normalized machine row and **4,000** report rows. The measured normalized table objects occupied **4,071,424 bytes**, compared with **11,091,968 bytes** for the report table object.

This 200,000-row synthetic workload did not show a meaningful case for keeping the denormalized table. If a real dashboard later has an expensive join and a measured read benefit, add a reporting copy only with transactional maintenance, a full rebuild/reconciliation path, and a visible last-refresh timestamp. The evidence is from one Windows-hosted run on 2026-11-12 (Python 3.14.9, SQLite 3.53.1); rerun it on the course laptop before making a hardware-specific claim.
