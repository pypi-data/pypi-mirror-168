import pandas as pd
import sqlite3
import json
import os
import zipfile
import sqlalchemy
from urllib.request import Request, urlopen
from pathlib import Path
from io import BytesIO
from loguru import logger


# Path to the package
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_PATH = Path(SCRIPT_DIR).parent.absolute()

# PharmGKB clinical/variant URLs
PHARMGKB_CLINICAL_ANNOTATIONS_URL = 'https://api.pharmgkb.org/v1/download/file/data/clinicalAnnotations.zip'
PHARMGKB_VARIANT_ANNOTATIONS_URL = 'https://api.pharmgkb.org/v1/download/file/data/variantAnnotations.zip'


def download_file(url: str) -> zipfile.ZipFile:
    logger.info(f"Downloading file {url}")
    request = Request(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
    )
    response = urlopen(request)
    zip = zipfile.ZipFile(BytesIO(response.read()))
    return zip


def create_sqlite_engine(name: str, print_logger: bool = True) -> sqlalchemy.engine.base.Engine:
    if print_logger:
        logger.info(f"Creating database {name} in {PACKAGE_PATH}/.cache")
    return sqlalchemy.create_engine(f'sqlite:////{PACKAGE_PATH}/.cache/{name}', echo=False)


def connect_to_database(name: str) -> sqlite3.Connection:
    if not os.path.exists(f"{PACKAGE_PATH}/.cache/{name}"):
        logger.error(f"Database {name} does not exist.")
        logger.info('\033[0m' + "Please use " + '\033[1m' + 'create_database' + '\033[0m' + " to create the database.")
        exit(1)
    return sqlite3.connect(f'{PACKAGE_PATH}/.cache/{name}')


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def save_json(data: dict, path: str):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def df_to_json(df: pd.DataFrame) -> dict:
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    return parsed


def drop_duplicated_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, ~df.columns.duplicated()]


def replace_to_underscore(df: pd.DataFrame, signs: list) -> pd.DataFrame:
    for sign in signs:
        df.columns = df.columns.str.replace(sign, '_')
    return df


def warn_about_no_genotype(variant: str, genotype: str):
    logger.warning(f"There is no {genotype} genotype in the database for {variant} variant.")


def warn_about_other_genotypes(variant: str):
    logger.info(f"There are other genotypes in the database for {variant} variant. Please check the variants_with_unknown_genotype.json file.")


def field_as_list(field: str, split_char: str) -> list:
    try:
        field = field.strip('"')
        field = field.replace(",\"", "\",\"", 1)
        field = field.replace("\",\"", ";")
        return field.split(split_char)
    except AttributeError:
        pass


def split_fields(df: pd.DataFrame, fields: list, split_char: str) -> list:
    for field in fields:
        df[field] = df[field].apply(lambda x: field_as_list(x, split_char))
    return df
