"""
Created on Thursday September 7 12:54:00 2017
@author: The KnowEnG dev team
lanier4@illinois.edu
"""
def select_subtype_df(run_parameters):
    """ get sub_spreadsheet_df and sub_phenotype_df of a phenotype category """
    from spreadsheets_transformation_toolbox import run_select_subtype_df
    run_select_subtype_df(run_parameters)

def common_samples_df(run_parameters):
    """ get common samples """
    from spreadsheets_transformation_toolbox import run_common_samples_df
    run_common_samples_df(run_parameters)

def select_genes_df(run_parameters):
    """ get spreadsheet from other spreadsheet with list of genes """
    from spreadsheets_transformation_toolbox import run_select_genes
    run_select_genes(run_parameters)

def merge_df(run_parameters):
    """ get the union of two dataframes """
    from spreadsheets_transformation_toolbox import run_merge_df
    run_merge_df(run_parameters)

def cluster_statistics_df(run_parameters):
    """ statistic by clustering """
    from spreadsheets_transformation_toolbox import run_cluster_statistics_df
    run_cluster_statistics_df(run_parameters)

def transpose_df(run_parameters):
    ''' transpose and write a spreadsheet'''
    from spreadsheets_transformation_toolbox import run_transpose
    run_transpose(run_parameters)

def numeric_transform(run_parameters):
    ''' numerical transformation of spreadsheet data '''
    from spreadsheets_transformation_toolbox import run_spreadsheet_numerical_transform
    run_spreadsheet_numerical_transform(run_parameters)

def stats_df(run_parameters):
    """ statistical data for a spreadsheet """
    from spreadsheets_transformation_toolbox import run_stats_df
    run_stats_df(run_parameters)


SELECT = {
    "select_subtype_df":select_subtype_df,
    "common_samples_df":common_samples_df,
    "select_genes_df":select_genes_df,
    "merge_df":merge_df,
    "cluster_statistics_df":cluster_statistics_df,
    "transpose_df":transpose_df,
    "numeric_transform":numeric_transform,
    "stats_df":stats_df}


def main():
    """
    This is the main function to perform sample clustering
    """
    import sys
    from knpackage.toolbox import get_run_directory_and_file
    from knpackage.toolbox import get_run_parameters

    run_directory, run_file = get_run_directory_and_file(sys.argv)
    run_parameters = get_run_parameters(run_directory, run_file)
    SELECT[run_parameters["method"]](run_parameters)


if __name__ == "__main__":
    main()
