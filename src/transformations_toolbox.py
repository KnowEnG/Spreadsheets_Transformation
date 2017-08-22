"""
lanier4@illinois.edu
(samples x phenotypes) spreadsheet transformations
"""
import os
import pandas as pd
import knpackage.toolbox as kn
import numpy as np

# utility
def read_a_list_file(input_file_name):
    """
    Args:
        input_file_name:     full path name of a file containing a list
    Returns:
        a list that is contained in the file
    """
    with open(input_file_name, 'r') as fh:
        str_input = fh.read()
    return list(str_input.split())


# transform_0
def transpose_df(spreadsheet_df):
    """ Transpose a spreadsheet data frame.
    Args:       
        spreadsheet_df: a pandas dataframe
    Returns:    
        spreadsheet_transpose_df: transposed dataframe
    """
    return spreadsheet_df.transpose()


def spreadsheet_transpose(run_parameters):
    """ Read, transpose a spreadsheet data frame, and write it to a new file.
    Args:
        run_parameters:     dict with the following keys:
            spreadsheet_file_name:    full path name of the input file
            results_directory:         where to write the output
    Returns:
        STATUS:             0 if written successfully
    """
    transform_name = '_T'
    input_file_name = os.path.abspath(run_parameters['spreadsheet_file_name'])
    results_directory = os.path.abspath(run_parameters['results_directory'])

    output_file_name = get_outfile_name(results_directory, input_file_name, transform_name)

    try:
        spreadsheet_df = pd.read_csv(input_file_name, sep='\t', index_col=0, header=0)
        spreadsheet_T_df = transpose_df(spreadsheet_df)
        spreadsheet_T_df.to_csv(output_file_name, sep='\t', index=True, header=True)
        return 0
    except:
        pass
        return -1


# transform_1
def get_common_samples_df(sxp_1_df, sxp_2_df):
    """Turn two dataframes with sample names in common into one with only the common samples in each. 
    Args:
        sxp_1_df:      samples x phenotypes dataframe (sxp_1_df = kn.get_spreadsheet_df(sxp_filename_1))
        sxp_2_df:      samples x phenotypes dataframe
    Returns:
        sxp_1_trim_df: samples x phenotypes with only sample names in both input dataframes
        sxp_2_trim_df: samples x phenotypes with only sample names in both input dataframes
    """
    sxp_1_gene_names = kn.extract_spreadsheet_gene_names(sxp_1_df)
    sxp_2_gene_names = kn.extract_spreadsheet_gene_names(sxp_2_df)
    common_samples_list = kn.find_common_node_names(sxp_1_gene_names, sxp_2_gene_names)

    return sxp_1_df.loc[common_samples_list], sxp_2_df.loc[common_samples_list]


def spreadsheets_common_samples(run_parameters):
    """ Read, turn two dataframes with sample names in common into one with only the common samples in each,
        and write them into new files.
    Args:
        run_parameters:     dict with the following keys:
            spreadsheet_1_file_name:   full path name of first input file
            spreadsheet_2_file_name:   full path name of second input file
            results_directory:         where to write the output
    Returns:                
        STATUS:                 0 if successful
    """
    transform_name = '_Common_Samples'
    results_directory = os.path.abspath(run_parameters['results_directory'])

    full_file_name_1 = run_parameters['spreadsheet_1_file_name']
    out_file_name_1 = get_outfile_name(results_directory, full_file_name_1, transform_name)

    full_file_name_2 = run_parameters['spreadsheet_2_file_name']
    out_file_name_2 = get_outfile_name(results_directory, full_file_name_2, transform_name)

    try:
        sxp_1_df = kn.get_spreadsheet_df(full_file_name_1)
        sxp_2_df = kn.get_spreadsheet_df(full_file_name_2)
        cs_df_1, cs_df_2 = get_common_samples_df(sxp_1_df, sxp_2_df)
        cs_df_1.to_csv(out_file_name_1, sep='\t', index=True, header=True)
        cs_df_2.to_csv(out_file_name_2, sep='\t', index=True, header=True)
        return 0
    except:
        pass
        return -1


# transform_2
def merge_df(spreadsheet_1_df, spreadsheet_2_df):
    """ Combine two spreadsheets into one with all samples and phenotypes. (NaN filled)
    Args:
        spreadsheet_1_df: samples x phenotypes dataframe
        spreadsheet_2_df: samples x phenotypes dataframe
    Returns:
        spreadsheet_union_df:         samples x phenotypes dataframe with combined samples and phenotypes
    """
    spreadsheet_X_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)
        
    return spreadsheet_X_df


def spreadsheets_merge(run_parameters):
    """Read, combine two spreadsheets into one with all samples and phenotypes(NaN filled), and write it into a new file.
    Args:
        run_parameters:         dict with the following keys:
            spreadsheet_1_file_name:   full path name of first input file
            spreadsheet_2_file_name:   full path name of second input file
            spreadsheet_merge_file_name:      output file name for input_path1
    Returns:
        STATUS:                 0 if successful
    """
    transform_name = '_Common_Samples'
    results_directory = os.path.abspath(run_parameters['results_directory'])

    file_name_1 = run_parameters['spreadsheet_1_file_name']
    d1, f1 = os.path.split(file_name_1)
    f1, nix_ext = os.path.splitext(f1)
    file_name_2 = run_parameters['spreadsheet_2_file_name']
    d2, f2 = os.path.split(file_name_2)
    f2, nix_ext = os.path.splitext(f2)
    f1_f2 = f1 + '_' + f2
    merge_file_name = get_outfile_name(results_directory, f1_f2, transform_name)

    try:
        spreadsheet_1_df = pd.read_csv(file_name_1, sep='\t', index_col=0, header=0)
        spreadsheet_2_df = pd.read_csv(file_name_2, sep='\t', index_col=0, header=0)
        spreadsheet_X_df = merge_df(spreadsheet_1_df,spreadsheet_2_df)

        spreadsheet_X_df.to_csv(merge_file_name, sep='\t', index=True, header=True)
        
        return 0
    
    except:
        pass
        return -1
    
# transform_3
def select_genes_df(spreadsheet_df, gene_select_list):
    """Turn one spreadsheet into one with only those genes selected from an input list.  
    Args:
        spreadsheet_df:             genes x samples data frame
        gene_select_list:           list of some gene names in the spreadsheet
    Returns:
        spreadsheet_intersected_df: data frame with only the genes in the intersection of input gene names.
    """
    gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_df)
    intersection_names = kn.find_common_node_names(gene_names, gene_select_list)
    return spreadsheet_df.loc[intersection_names]


def select_spreadsheet_genes(run_parameters):
    """Read, turn one spreadsheet into one with only those genes selected from an input list, and write it to a new file. 
    Args:
        run_parameters:     dict with the following keys:
            spreadsheet_file_name: full path name of first input file(spreadsheet)
            gene_list_file_name: full path name of second input file(gene selection list)
            spreadsheet_genes_selected_file_name:  full path name of output file
    Returns:
        STATUS:                 0 if successful
    """
    transform_name = '_Gene_List'
    results_directory = os.path.abspath(run_parameters['results_directory'])

    spreadsheet_file = run_parameters['spreadsheet_file_name']
    gene_select_list = read_a_list_file(spreadsheet_file)

    out_file_name = get_outfile_name(results_directory, spreadsheet_file, transform_name)
    try:
        spreadsheet_df = pd.read_csv(spreadsheet_file, sep='\t', index_col=0, header=0)
        spreadsheet_intersected_df = select_genes_df(spreadsheet_df, gene_select_list)
        spreadsheet_intersected_df.to_csv(out_file_name , sep='\t', index=True, header=True)
        return 0
    except:
        return -1


def cluster_averages(spreadsheet_df,labels_df):
    """Return a dataframe of averages for each category given a genes x samples dataframe and
        a samples classification dictionary
    Args:
        spreadsheet_df:   a genes x samples dataframe
        labels_df:        a samples classification dictionary
    Returns:
        cluster_ave_df:   a dataframe of averages for each category
    """
    labels_dict = labels_df.to_dict()['cluster_number']
    cluster_numbers = list(np.unique(list(labels_dict.values())))
    labels = list(labels_dict.values())
    cluster_ave_df = pd.DataFrame({i: spreadsheet_df.iloc[:, labels == i].mean(axis=1) for i in cluster_numbers})
    return cluster_ave_df
    
    
def spreadsheet_clustering_averages(run_parameters):
    """Read, return a dataframe of averages for each catagory given a genes x samples dataframe and
        a samples classification dictionary, and write it into a new file.
    Args:
        run_parameters:                              dict with the following keys:
            spreadsheet_file_name:                   full path name of the first input file(genes x samples dataframe)
            sample_classification_dict_file_name:    full path of the second input file(samples classification dict)
            spreadsheet_cluster_averages_file_name:  full path name of the output file
    Returns:
        STATUS:                 0 if successful
    """
    transform_name = '_Clustering_Averages'
    results_directory = os.path.abspath(run_parameters['results_directory'])

    spreadsheet_file_name = run_parameters['spreadsheet_file_name']
    sample_labels_file_name = run_parameters['sample_labels_file_name']

    spreadsheet_averages_file_name = get_outfile_name(results_directory, spreadsheet_file_name, transform_name)
    try:
        spreadsheet_df = pd.read_csv(spreadsheet_file_name, sep='\t', index_col=0, header=0)
        labels_df = pd.read_csv(sample_labels_file_name, sep='\t',
                                index_col=0, names=['sample','cluster_number'])

        cluster_ave_df = cluster_averages(spreadsheet_df,labels_df)
        cluster_ave_df.to_csv(spreadsheet_averages_file_name, sep='\t', index=True, header=True)
        return 0
    except:
        return -1

    
def select_categorical_df(spreadsheet_df,phenotype_df,phenotype_id,select_category):
    """From a genes x samples spreadsheet and a samples x phenotypes spreadsheet, return both spreadsheets
        with only the samples corresponding to a category in a phenotype.
    Args:
        spreadsheet_df:    a genes x samples dataframe
        phenotype_df       a samples x phenotypes dataframe
        phenotype_id
        select_category
    Returns:
        spreadsheet_category_df:    genes x samples dataframe with only the samples corresponding to a category in pheno
        phenotype_category_df:      samples x phenotypes dataframe with only the samples corresponding to a category
    """
    samples_list = phenotype_df.index[phenotype_df[phenotype_id] == select_category]
    # print(phenotype_df[phenotype_id][2])
    # print(samples_list)
    phenotype_category_df = phenotype_df.loc[samples_list]
    
    spreadsheet_category_df = spreadsheet_df[samples_list]
    return spreadsheet_category_df, phenotype_category_df


def spreadsheet_select_pheno_categorical(run_parameters):
    """ Read, from a genes x samples spreadsheet and a samples x phenotypes spreadsheet,
        return both spreadsheets with only the samples corresponding to a category in a phenotype,
        and write them to new files.
    Args:
        run_parameters:                                  dict with the following keys:
            genes_samples_spreadsheet_file_name:         full path name of the first input file(genes x samples df)
            samples_phenotypes_spreadsheet_file_name:    full path name of second input file(samples x phenoytpes df)
            catetorical_spreadsheet_file_name:           full path name of the first output file
            categorical_phenotypes_file_name:            full path name of the second output file
    Returns:
        STATUS:                 0 if successful
    
    """
    transform_name = '_Select_Categorical'
    results_directory = os.path.abspath(run_parameters['results_directory'])

    genes_samples_spreadsheet_file_name = run_parameters['genes_samples_spreadsheet_file_name']
    samples_phenotypes_spreadsheet_file_name = run_parameters['samples_phenotypes_spreadsheet_file_name']
    phenotype_id = run_parameters['phenotype_id']
    select_category = run_parameters['select_category']

    gene_samples_outfile = get_outfile_name(results_directory, genes_samples_spreadsheet_file_name, transform_name)
    samples_phenotypes_outfile = get_outfile_name(results_directory,
                                                  samples_phenotypes_spreadsheet_file_name, transform_name)
    try:
        spreadsheet_df = pd.read_csv(genes_samples_spreadsheet_file_name, sep='\t', index_col=0, header=0)
        phenotype_df = pd.read_csv(samples_phenotypes_spreadsheet_file_name, sep='\t', index_col=0, header=0)
        spreadsheet_category_df, phenotype_category_df  = select_categorical_df(spreadsheet_df,
                                                                                phenotype_df,
                                                                                phenotype_id,
                                                                                select_category)
        spreadsheet_category_df.to_csv(gene_samples_outfile, sep='\t', index=True, header=True)
        phenotype_category_df.to_csv(samples_phenotypes_outfile, sep='\t', index=True, header=True)
        return 0
    except:
        return -1


def get_outfile_name(destination_dir, spreadsheet_file_name, transform_name, file_ext='.tsv'):
    """ construct a full path output file name from destination path, spreadsheet file name,
        transformation name and file extenstion
     Args:
         destination_dir:
         spreadsheet_file_name:
         transform_name:
         file_ext:
    Returns:
        spreadsheet_transformed_file_name: full path output file name
    """
    nix_dir, spreadsheet_transformed_file_name = os.path.split(spreadsheet_file_name)
    spreadsheet_transformed_file_name, nix_ext = os.path.splitext(spreadsheet_transformed_file_name)
    spreadsheet_transformed_file_name = spreadsheet_transformed_file_name + transform_name + file_ext
    spreadsheet_transformed_file_name = os.path.join(destination_dir, spreadsheet_transformed_file_name)
    return spreadsheet_transformed_file_name