# ISEQPHARMGKB

Scripts that allow you to:
1) Create databases (clinical and variant) from [PharmGKB](https://www.pharmgkb.org/) 
2) Get clinical or variant annotations from PharmGKB for own queries

## Install iseqpharmgkb library

Optional steps (create virtual environment):
```
python3 -m venv venv
source venv/bin/activate
```

Obligatory steps:
```
python3 -m pip install --upgrade pip
pip install iseqpharmgkb
```

## Requirements

- python >=3.6
- pandas >= 1.2.4
- requests >= 2.22.0
- SQLAlchemy >= 1.3.17

## Create databases

```
create_database
```

## Get clinical annotations

```
get_clinical_annotation --queries /path/to/query.json --output-filename /output/filename.json
```

An example `query.json` file should look like this:
```
{
    "rs1050828": "CC",
    "rs5030868": "CC",
    "CYP2D6*2": "*2",
    "CYP2D6*1": "*1/*1"
}
```

## Get variant annotations

```
get_variant_annotation --queries /path/to/query.json --output-filename /output/filename.json
```

An example `query.json` file should look like this:
```
{
    "rs1050828": "CC",
    "rs5030868": "CC",
    "CYP2D6*2": "*2",
    "CYP2D6*1": "*1/*1"
}
```