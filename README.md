# Python Automation Toolkit

A collection of safe, reusable command-line automation utilities. The main utility scans a folder and creates a report of files grouped by extension; an optional mode can organize files after preview.

## Features
- Dry-run preview by default.
- Extension-based grouping.
- Collision-safe filenames.
- CSV inventory report.
- Optional file moves with `--apply`.
- Recursive scan option.

## Requirements
Python 3.10+; standard library only.

## Run
```bash
python main.py /path/to/folder
python main.py /path/to/folder --report output/inventory.csv
python main.py /path/to/folder --apply
python main.py /path/to/folder --recursive --apply
```

The program never moves files unless `--apply` is explicitly provided. Try it on a test folder first. Use only folders you own or are authorized to manage.

## Tests
```bash
python -m unittest discover -s tests -v
```
