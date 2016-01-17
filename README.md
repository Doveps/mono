# Bassist
The bassist reads output produced by the `scanner` and calculates the
baseline for a host, plus modifications made to that host.

# Usage
* Find out where your scanner put its output (for example:
`~/doveps/scanner/local/33.33.33.50`).
* Start up your Neo4j db (currently we assume it's running on localhost,
  port 7474).

## Create Automation
Specify scanner results directory and the automation code output
directory:
`create_automation -s ~/doveps/scanner/local/33.33.33.51/ -c ~/doveps`

If this says you should run savant-web, run savant-web and then re-run
`create_automation` as above.

# Setup
Bassist currently runs in Python 2.

## OS X
```sh
pip install -r requirements.txt
```

# Testing
`bassist` tests using pytest and optionally pytest-cov. For the former:

```
pip install pytest
py.test
```

## Coverage
To also test code coverage:

```
pip install pytest-cov
py.test --cov-report html --cov-config .coveragerc --cov .
```

The test report is in the `htmlcov` directory; use a web browser to view it.

# TODO
* Support Python 3
