"""
Created on Wed Jul 20 14:47:45 2016
@author: The KnowEnG dev team
"""

def spreadsheet_transpose(run_parameters):
    '''nmf clustering'''
    from transformations_toolbox import spreadsheet_transpose
    spreadsheet_transpose(run_parameters)

def spreadsheets_common_samples(run_parameters):
    from transformations_toolbox import spreadsheets_common_samples
    spreadsheets_common_samples(run_parameters)

def spreadsheets_merge(run_parameters):
    from transformations_toolbox import spreadsheets_merge
    spreadsheets_merge(run_parameters)

def select_spreadsheet_genes(run_parameters):
    from transformations_toolbox import select_spreadsheet_genes
    select_spreadsheet_genes(run_parameters)

def spreadsheet_clustering_averages(run_parameters):
    from transformations_toolbox import spreadsheet_clustering_averages
    spreadsheet_clustering_averages(run_parameters)

def spreadsheet_select_pheno_categorical(run_parameters):
    from transformations_toolbox import spreadsheet_select_pheno_categorical
    spreadsheet_select_pheno_categorical(run_parameters)

SELECT = {
    "spreadsheet_transpose": spreadsheet_transpose,
    "spreadsheets_common_samples": spreadsheets_common_samples,
    "spreadsheets_merge": spreadsheets_merge,
    "select_spreadsheet_genes": select_spreadsheet_genes,
    "spreadsheet_clustering_averages": spreadsheet_clustering_averages,
    "spreadsheet_select_pheno_categorical": spreadsheet_select_pheno_categorical}

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
