#!/usr/bin/env python3

import argparse
import pandas as pd
import os
from utils import utils


__version__ = '0.0.1'


def create_clinical_database():
    engine = utils.create_sqlite_engine("clinical.db")
    clinical_annotations_zip = utils.download_file(utils.PHARMGKB_CLINICAL_ANNOTATIONS_URL)
    for file in clinical_annotations_zip.namelist():
        if file.endswith(".tsv"):
            df = pd.read_csv(clinical_annotations_zip.open(file), sep="\t", error_bad_lines=False, warn_bad_lines=False)
            df = utils.replace_to_underscore(df, signs=[" ", "/"])
            df.to_sql(file.split(".tsv")[0], con=engine, if_exists='replace', index=False)


def create_variant_database():
    engine = utils.create_sqlite_engine("variant.db")
    variant_annotations_zip = utils.download_file(utils.PHARMGKB_VARIANT_ANNOTATIONS_URL)
    for file in variant_annotations_zip.namelist():
        if file.endswith(".tsv"):
            df = pd.read_csv(variant_annotations_zip.open(file), sep="\t", error_bad_lines=False, warn_bad_lines=False)
            df = utils.replace_to_underscore(df, [" ", "/"])
            df.to_sql(file.split(".tsv")[0], con=engine, if_exists='replace', index=False)


def main():
    parser = argparse.ArgumentParser(description='Create databases from PharmGKB data')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    if not os.path.exists(f"{utils.PACKAGE_PATH}/.cache"):
        os.mkdir(f"{utils.PACKAGE_PATH}/.cache")

    # create clinical database
    create_clinical_database()

    # create variant database
    create_variant_database()


if __name__ == '__main__':
    main()
