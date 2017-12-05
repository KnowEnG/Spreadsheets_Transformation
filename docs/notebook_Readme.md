# KnowEnG's Spreadsheets Transformation Jupyter notebook

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

# Using the KnowEnG Spreadsheets_Transformation.ipynb notebook.
 ---
## 1) Start the notebook code:
 ---
 
### If your browser allows auto-initialization you will see this screen.
<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

### If not, and the code is showing, use the _Cell_ menu to _Run All_

<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

### Click on the **View** button to see the top of the phenotype file.
<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

### Use listboxes to select columns for: ClusterID, Event and Time; click the **Show** button.
<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

### Use the _Kernel_ menu _Restart and Clear Output_ to clear error messages (and all output).

<p align="center">
  <img  src="../data/images/select_restart.png" height=220>
</p>

## 2) Example Transpose a file Using the default data:
 ---

### Click on the **View** button to see the top of the spreadsheet file.
<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

### Click on the **View** button to see the top of the spreadsheet file.
<p align="center">
  <img  src="../data/images/Intersection.png" height=220>
</p>

## 3) Upload, view and transform your data:
 ---


### Use the _File_ menu _Open_ to open the _user_data_ directory.
