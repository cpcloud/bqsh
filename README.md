# `bqsh`: BigQuery interactive shell

`bqsh` is an interactive shell for BigQuery.

Install by cloning the repo and run `python setup.py install`

Usage:

```
$ bqsh
usage: bqsh [-h] [-H HISTORY_FILE] [-C] [-m] [-v] [-c] project dataset
```

Examples:


```sh
$ bqsh ibis-gbq testing
ibis-gbq.testing > select * from testing.functional_alltypes limit 5
```
