# Injection self-test

Complete against the actual final-project interface before peer review.

## Code audit
- Search performed for f-strings, percent formatting, concatenated SQL and dynamically assembled SQL:
- Files reviewed:
- Every query accepting user/external input uses bound parameters: [Yes/No]
- Any exceptions and why they are safe:

## Deliberately malicious input
Use a harmless SQL-injection test string in every user-facing field, for example:
' OR 1=1 --

- Field tested:
- Expected safe behavior:
- Actual behavior:
- Did the input return unauthorized rows, alter schema or change stored data?
- Evidence/output:

## Fixes
- Vulnerable code found:
- Parameterized replacement:
- Commit:
