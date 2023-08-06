#!/usr/bin/env python3

from pharmgkb.create_database import *


def test_create_clinical_database():
    # create clinical database
    create_clinical_database()

    # check if clinical.db exists
    assert os.path.exists(f"{utils.PACKAGE_PATH}/.cache/clinical.db")

    # check if clinical.db has tables
    engine = utils.create_sqlite_engine("clinical.db", print_logger=False)
    assert engine.table_names() == ['clinical_ann_alleles', 'clinical_ann_evidence', 'clinical_ann_history', 'clinical_annotations']

    # check if clinical.db has data
    for table in engine.table_names():
        df = pd.read_sql_table(table, engine)
        assert not df.empty

    
def test_create_variant_database():
    # create variant database
    create_variant_database()

    # check if variant.db exists
    assert os.path.exists(f"{utils.PACKAGE_PATH}/.cache/variant.db")

    # check if variant.db has tables
    engine = utils.create_sqlite_engine("variant.db", print_logger=False)
    assert engine.table_names() == ['study_parameters', 'var_drug_ann', 'var_fa_ann', 'var_pheno_ann']

    # check if variant.db has data
    for table in engine.table_names():
        df = pd.read_sql_table(table, engine)
        assert not df.empty


if __name__ == '__main__':
    test_create_clinical_database()
    test_create_variant_database()
