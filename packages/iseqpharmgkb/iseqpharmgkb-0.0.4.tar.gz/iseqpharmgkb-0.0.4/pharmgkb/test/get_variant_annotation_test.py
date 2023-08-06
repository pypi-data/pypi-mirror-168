#!/usr/bin/env python3

from pharmgkb.get_variant_annotation import *


def test_get_variant_annotation():
    # load queries
    queries = utils.load_json("query.json")

    # connect to database
    database = utils.connect_to_database("variant.db")

    # get variant annotation
    output = get_variant_annotation(queries, database)

    # check if output["G6PD"] has 1 element
    assert len(output["G6PD"]) == 1

    # check if rs1050828 has 1 element
    assert len(output["G6PD"]["rs1050828"]) == 1

    # check if Variant_Annotation_ID for rs1050828 is 1183705675
    assert output["G6PD"]["rs1050828"][0]["Variant_Annotation_ID"] == 1183705675

    # check if 1st element of CYP2D6*1 variant is equal to the expected output
    assert output["CYP2D6"]["CYP2D6*1"][0] == {
        "Variant_Annotation_ID": 1183632366,
        "Variant_Haplotypes": "CYP2D6*1, CYP2D6*4",
        "Gene": [
          "CYP2D6"
        ],
        "Drug(s)": [
          "codeine"
        ],
        "PMID": 19940985,
        "Phenotype_Category": "Metabolism/PK",
        "Significance": "yes",
        "Notes": "Lower plasma concentrations of the morphine metabolite M3G and undetectable levels of M6G were found in the two poor metabolizers (*4/*4) compared to extensive metabolizers (*1/*1 +*1/*4). PM were determined on the basis of their CYP2D6*3, *4, and *6 alleles.",
        "Sentence": "CYP2D6 *4/*4 is associated with decreased metabolism of codeine in people with Kidney Failure, Chronic as compared to CYP2D6 *1/*1 + *1/*4.",
        "Alleles": "*4/*4",
        "Specialty_Population": None
    }


if __name__ == '__main__':
    test_get_variant_annotation()