# KnowEnG's Spreadsheets Transformation Jupyter notebook-operation of pipeline 

This is the Knowledge Engine for Genomics (KnowEnG), an NIH BD2K Center of Excellence, Spreadsheets Transformation Pipeline.

This pipeline applies various transformations to one or more Spreadsheets (Genomic, Phenotypic, ...)

There are eight transformation methods that one can choose from:

| **Options**                                      | **Method**                           | **Parameters**       |
| ------------------------------------------------ | -------------------------------------| -------------------- |
| Subset Based on Phenotype category and id        | select subtype                 | spreadsheet, phenotype, id, category|
| Intersection                                     | common samples                       | two spreadsheets     |
| Subset Genes                                     | select genes                         | spreadsheet, list     |
| Union                                            | merge                                | two spreadsheets     |
| Group Then Apply a Function                      | cluster statistics                   | spreadsheet, labels   |
| Spreadsheet numerical transform                  | numerical transform            | spreadsheet, transformation name|
| Spreadsheet statistics                           | stats                          | spreadsheet, statistic name|
| Spreadsheet transpose                            | run_transpose                        | one spreadsheet |

## Table of Transformtions
---
1. Subset Based on Phenotype category and id
2. Intersection
3. Subset Genes
4. Union
5. Group then apply a function
6. Spreadsheet numerical transform
7. Spreadsheet statistics
8. Spreadsheet transpose
