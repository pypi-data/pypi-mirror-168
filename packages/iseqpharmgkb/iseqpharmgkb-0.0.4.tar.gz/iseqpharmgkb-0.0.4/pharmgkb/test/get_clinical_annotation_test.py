#!/usr/bin/env python3

from pharmgkb.get_clinical_annotation import *


def test_get_clinical_annotation():
    # load queries
    queries = utils.load_json("query.json")

    # connect to database
    database = utils.connect_to_database("clinical.db")

    # get variant annotation
    output, logs = get_clinical_annotation(queries, database)

    # check if output["G6PD"] has 1 element
    assert len(output["G6PD"]) == 1

    # check if rs1050828 has 3 elements
    assert len(output["G6PD"]["rs1050828"]) == 3

    # check if Clinical_Annotation_ID for rs1050828 is 1183619864
    assert output["G6PD"]["rs1050828"][0]["Clinical_Annotation_ID"] == 1183619864

    # check if for rs5030868 there are 5 genotypes other than in query
    assert len(logs["G6PD"]["rs5030868"]) == 5

    # check if for rs5030868 other genotypes are ['A', 'AA', 'AG', 'G', 'GG']
    assert [item["Genotype_Allele"] for item in logs["G6PD"]["rs5030868"]] == ['A', 'AA', 'AG', 'G', 'GG']

    # check if 1st element of CYP2D6*1 variant is equal to the expected output
    assert output["CYP2D6"]["CYP2D6*1"][0] == {
        "Clinical_Annotation_ID": 1183690410,
        "Genotype_Allele": "*1/*1",
        "Annotation_Text": "Patients with two functional CYP2D6 alleles who are treated with aqueous timolol may have decreased exposure to timolol and less excerice heart rate reduction as compared to patients with two non-functional CYP2D6 allele. Other genetic and clinical factors may also influence a patient's response to aqueous timolol.",
        "Allele_Function": None,
        "Variant_Haplotypes": "CYP2D6*1, CYP2D6*3, CYP2D6*4, CYP2D6*5",
        "Gene": [
          "CYP2D6"
        ],
        "Level_of_Evidence": "3",
        "Level_Override": None,
        "Level_Modifiers": "Tier 1 VIP",
        "Score": 1.75,
        "Phenotype_Category": "Other",
        "PMID_Count": 2,
        "Evidence_Count": 2,
        "Drug(s)": [
          "timolol"
        ],
        "Phenotype(s)": None,
        "Latest_History_Date_(YYYY-MM-DD)": "2021-03-24",
        "URL": "https://www.pharmgkb.org/clinicalAnnotation/1183690410",
        "Specialty_Population": None
    }


if __name__ == '__main__':
    test_get_clinical_annotation()