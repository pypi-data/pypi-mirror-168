#!/usr/bin/env python3

import argparse
import pandas as pd
import sqlite3
from utils import utils


def get_variant_annotation(queries: dict, database: sqlite3.Connection) -> dict:
    output = dict()
    for variant, genotype in queries.items():
        df = pd.read_sql(f'''SELECT * FROM var_drug_ann 
            WHERE (Variant_Haplotypes LIKE "%{variant},%"
            OR Variant_Haplotypes LIKE "%{variant}")''', database)
        # df to json
        if not df.empty:
            df = utils.split_fields(df=df, fields=["Gene", "Drug(s)"], split_char=";")
            try:
                gene = df["Gene"].tolist()[0][0]
            except TypeError:
                gene = variant
            if gene in output:
                output[gene][variant] = utils.df_to_json(df)
            else:
                output[gene] = {variant: utils.df_to_json(df)}
    return output


def main():
    parser = argparse.ArgumentParser(description='Get variant annotation from PharmGKB')
    parser.add_argument('--queries', type=str, required=True, help='Json file with queries to db')
    parser.add_argument('--output-filename', type=str, required=True, help='Output filename')
    args = parser.parse_args()

    # load queries
    queries = utils.load_json(args.queries)

    # connect to database
    database = utils.connect_to_database("variant.db")

    # get variant annotation
    output = get_variant_annotation(queries, database)

    # save output
    utils.save_json(output, args.output_filename)


if __name__ == '__main__':
    main()
