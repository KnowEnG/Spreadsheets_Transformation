"""
lanier4@illinois.edu
for KnowEnG pipelines
"""

import os
import string

import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from   lifelines import KaplanMeierFitter
from   lifelines.statistics import multivariate_logrank_test

from scipy import stats
import knpackage.toolbox as kn

def run_categorical_binary(run_parameters):
    """ save a samples vs category binary spreadsheet

    Args:
        run_parameters: with keys:
                        results_directory
                        phenotype_file_name
                        column_id
    Returns:
        Only writes the samples phenotype category binary as a .tsv
    """
    transform_name = 'categorical_binary'
    results_directory = run_parameters['results_directory']
    phenotype_file_name = run_parameters['phenotype_file_name']
    column_id = run_parameters['column_id']

    clust_file_names = phenotype_file_name.split(',')
    if isinstance(clust_file_names, list) and len(clust_file_names) > 1:
        clust_file_list = []
        data_dir = ''
        for cf in clust_file_names:
            data_dir_x, cf_name = os.path.split(cf)
            clust_file_list.append(cf_name)
            if data_dir == '':
                data_dir = data_dir_x


        cat_bin_df = get_cluster_binary_dataframe(clust_file_list, data_dir)
        outfile_name = get_outfile_name(results_directory, 'CLUSTERS', transform_name, 'tsv', False)
        cat_bin_df.to_csv(outfile_name, sep='\t')
        # write_transform_df(cat_bin_df, 'clusters', transform_name, results_directory)

    else:
        category_df = kn.get_spreadsheet_df(phenotype_file_name).fillna('NaN')
        cat_bin_df = select_categorical_binary(category_df, column_id)

        write_transform_df(cat_bin_df, phenotype_file_name, transform_name, results_directory)


def select_categorical_binary(category_df, column_id):
    """
    Args:
    Returns:

    """
    if isinstance(category_df, str) and os.path.isfile(category_df):
        category_df = kn.get_spreadsheet_df(category_df).fillna('NaN')
        # legacy protection
        
    column_values = category_df[column_id]
    cat_names = np.unique(column_values)
    cat_bin_df = pd.DataFrame(np.zeros((category_df.shape[0], len(cat_names))), columns=cat_names, index=category_df.index)

    for column_k in cat_names:
        cat_bin_df[column_k] += category_df[column_id] == column_k

    return cat_bin_df


def get_categorical_binary_df(category_df, column_id):
    """
    Args:
        category_df:    samples x phenotypes dataframe
        column_id:      which column to covert to binary

    Returns:
        cat_bin_df:     samples x phenotypes dataframe with binary membership columns
    """
    column_values = category_df[column_id]
    cat_names = np.unique(column_values)
    cat_bin_df = pd.DataFrame(np.zeros((category_df.shape[0], len(cat_names))),
                              columns=cat_names, index=category_df.index)

    for column_k in cat_names:
        cat_bin_df[column_k] += category_df[column_id] == column_k

    return cat_bin_df


def integer_2_alphanumeric_sequence(alpha_set, n, width=None):
    """ convert integer n to base alpha_set numbering """
    alpha_set = sorted(list(set(list(alpha_set))))
    alpha_base = len(alpha_set)
    if width is None:
        max_p = 0
        while n - alpha_base ** max_p > 0:
            max_p += 1
    else:
        max_p = width - 1

    S = ''
    alpha_exponent = 1
    for alpha_exponent in range(max_p, 0, -1):
        S += alpha_set[np.mod(int(np.floor(n / alpha_base ** alpha_exponent)), alpha_base)]

    last_index = int(np.floor(n - alpha_base ** alpha_exponent))
    S += alpha_set[np.mod(last_index, alpha_base)]

    return S


def get_alpha_sequence_name(left_name, n_dex):
    """ construct alphabetically numbered, sortable name from "left_name" prefix and "_AA" suffix
    """
    ALPHA_CAPS = string.ascii_letters[26:]
    alpha_seq = integer_2_alphanumeric_sequence(ALPHA_CAPS, n_dex, width=2)

    return left_name + '_' + alpha_seq


def get_df_names(dataframe_dict):
    """ usage: row_names_dict, rows_list, col_names_dict, columns_list = get_df_names(dataframe_dict)
    get a dict of column names """
    col_set = set()
    col_names_dict = {}
    row_set = set()
    row_names_dict = {}
    df_names_list = []
    for df_name, df in dataframe_dict.items():
        df_names_list.append(df_name)
        col_names_dict[df_name] = list(df.columns)
        col_set = col_set | set(list(df.columns))
        row_names_dict[df_name] = list(df.index)
        row_set = row_set | set(df.index.tolist())

    columns_list = sorted(list(col_set))
    rows_list = sorted(list(row_set))
    df_names_list = sorted(df_names_list)

    return row_names_dict, rows_list, col_names_dict, columns_list, df_names_list


def get_cluster_binary_dataframe(file_names_list, data_dir=None):
    """ get a dictionay of dataframes from a list of dataframe files """
    INDEX_COL_NAME = 'sample_id'
    DF_BASE_NAME = 'sample'

    if data_dir is None:
        data_dir = os.getcwd()

    dataframes_dict = {}
    count = 0

    for file_name in file_names_list:
        full_path_name = os.path.join(data_dir, file_name)

        this_name = get_alpha_sequence_name(DF_BASE_NAME, count)
        count += 1

        this_df = pd.read_csv(full_path_name, sep='\t', index_col=0, header=None)
        this_df.columns = ['clusters']
        this_df.index.name = INDEX_COL_NAME
        dataframes_dict[this_name] = get_categorical_binary_df(this_df, 'clusters')

    row_names_dict, rows_list, col_names_dict, columns_list, df_names_list = get_df_names(dataframes_dict)
    cluster_binary_dataframe = pd.DataFrame(data=None, index=rows_list)
    cluster_binary_dataframe.index.name = INDEX_COL_NAME
    for col_name in columns_list:
        for df_name in df_names_list:
            df_cols_name = col_names_dict[df_name]
            if col_name in df_cols_name:
                new_col_name = df_name + '_%s' % (col_name)
                cluster_binary_dataframe[new_col_name] = 0
                col_data_df = dataframes_dict[df_name]
                cluster_binary_dataframe.loc[row_names_dict[df_name], new_col_name] = col_data_df[col_name]

    return cluster_binary_dataframe


def run_kaplan_meier(run_parameters):
    """ save the lifelines kaplan-meier graphical analysis and p-value to two files

    Args:
        run_parameters: with keys:
                        results_directory
                        phenotype_file_name (containing the following column names)
                        cluster_id
                        event_id
                        time_id

    Returns:
        Writes:         two time-stamped files named after the phenotype file and "kaplan-meier"
                        "png" (640 x 480) image of the lifelines kaplan-meier graphical analysis
                        one cell dataframe with the p-value of the multivariate logrank test
    """
    results_directory = run_parameters['results_directory']
    phenotype_file_name = run_parameters['phenotype_file_name']
    cluster_id = run_parameters['cluster_id']
    event_id = run_parameters['event_id']
    time_id = run_parameters['time_id']

    phenotype_df = kn.get_spreadsheet_df(phenotype_file_name)

    T = phenotype_df[time_id]
    C = phenotype_df[event_id]

    results = multivariate_logrank_test(T, phenotype_df[cluster_id], C, alpha=0.99)
    p_value = str('%g' % (results.p_value))
    test_name = 'multivariate_logrank_test'

    Clusters = sorted(phenotype_df[cluster_id].unique())
    num_clusters = len(Clusters)

    plt.clf()
    ax = plt.subplot(111)

    kmf = KaplanMeierFitter()
    for cluster in Clusters:
        ixc = phenotype_df[cluster_id] == cluster
        kmf.fit(T.ix[ixc], C.ix[ixc], label=cluster + 1)
        kmf.plot(ax=ax, show_censors=True, ci_show=False)

    plt.title('number of clusters = %s' % (num_clusters))
    plt.xlabel('Time (days)')
    plt.ylabel('OS')

    transform_name = "kaplan_meier"
    kaplan_meier_spreadsheet_df = pd.DataFrame(data=p_value, index=[test_name], columns=['p_value'])

    write_transform_df(kaplan_meier_spreadsheet_df, phenotype_file_name, transform_name + '_p_value', results_directory)
    result_name = get_outfile_name(results_directory, phenotype_file_name, transform_name + '_graphic', file_ext='png')
    plt.savefig(result_name, dpi=100)


def run_select_subtype_df(run_parameters):
    """ Subset samples based on some row value, e.g., patients with longer survival.
        Output can be a smaller spreadsheet with fewer columns.
        From a genes x samples spreadsheet and a samples x phenotypes spreadsheet,
        return both spreadsheets with only the samples corresponding to a category in a phenotype.

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name", "phenotype_file_name",
                    "phenotype_id", "select_category"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_file_name = run_parameters['spreadsheet_file_name']
    phenotype_file_name = run_parameters['phenotype_file_name']
    phenotype_id = run_parameters['phenotype_id']
    select_category = run_parameters['select_category']

    spreadsheet_df = kn.get_spreadsheet_df(spreadsheet_file_name)
    phenotype_df = kn.get_spreadsheet_df(phenotype_file_name)

    spreadsheet_df, phenotype_df = select_subtype_df(spreadsheet_df, phenotype_df, phenotype_id, select_category)

    transform_name = "phenotype_category"
    write_transform_df(spreadsheet_df, spreadsheet_file_name, transform_name, results_directory)
    write_transform_df(phenotype_df, phenotype_file_name, transform_name, results_directory)


def select_subtype_df(spreadsheet_df, phenotype_df, phenotype_id, select_category):
    """ From a genes x samples spreadsheet and a samples x phenotypes spreadsheet, return both spreadsheets
        with only the samples corresponding to a category in a phenotype.

    Args:
        spreadsheet_df:          genes x samples dataframe
        phenotype_df:            samples x phenotypes dataframe
        phenotype_id:            column name in spreadsheet_df, row name in phenotype_df
        select_category:         one of the possible phenotype_id values

    Returns:
        spreadsheet_category_df: genes x samples dataframe with only the samples corresponding to a category in pheno
        phenotype_category_df:   samples x phenotypes dataframe with only the samples corresponding to a category
    """
    samples_list = sorted(phenotype_df.index[phenotype_df[phenotype_id] == select_category])
    phenotype_category_df = phenotype_df.loc[samples_list]
    samples_list = sorted(list(set(samples_list) & set(spreadsheet_df.columns)))
    spreadsheet_category_df = spreadsheet_df[samples_list]

    return spreadsheet_category_df, phenotype_category_df


def run_common_samples_df(run_parameters):
    """ Make two spreadsheets consistent by samples: two new spreadsheets created
        with samples being the intersection of sample sets of given spreadsheets.

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_1_file_name", "spreadsheet_2_file_name"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_1_file_name = run_parameters['spreadsheet_1_file_name']
    spreadsheet_2_file_name = run_parameters['spreadsheet_2_file_name']

    spreadsheet_1_df = kn.get_spreadsheet_df(spreadsheet_1_file_name)
    spreadsheet_2_df = kn.get_spreadsheet_df(spreadsheet_2_file_name)

    spreadsheet_1_df, spreadsheet_2_df = common_samples_df(spreadsheet_1_df, spreadsheet_2_df)

    transform_name = "common_samples"
    write_transform_df(spreadsheet_1_df, spreadsheet_1_file_name, transform_name, results_directory)
    write_transform_df(spreadsheet_2_df, spreadsheet_2_file_name, transform_name, results_directory)


def common_samples_df(spreadsheet_1_df, spreadsheet_2_df):
    """ Make two spreadsheets consistent by samples: two new spreadsheets created
        with samples being the intersection of sample sets of given spreadsheets.

    Args:
        spreadsheet_1_df:      samples x phenotypes dataframe (spreadsheet_1_df = kn.get_spreadsheet_df(spreadsheet_filename_1))
        spreadsheet_2_df:      samples x phenotypes dataframe

    Returns:
        spreadsheet_1_trim_df: samples x phenotypes with only sample names in both input dataframes
        spreadsheet_2_trim_df: samples x phenotypes with only sample names in both input dataframes
    """
    spreadsheet_1_gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_1_df)
    spreadsheet_2_gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_2_df)
    common_samples_list = kn.find_common_node_names(spreadsheet_1_gene_names, spreadsheet_2_gene_names)

    return spreadsheet_1_df.loc[common_samples_list], spreadsheet_2_df.loc[common_samples_list]


def run_select_genes(run_parameters):
    """ Subset genes based on given gene set. Output is a spreadsheet with fewer rows

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name", "gene_list_file_name"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_file_name = run_parameters['spreadsheet_file_name']
    gene_list_file_name = run_parameters['gene_list_file_name']

    spreadsheet_df = kn.get_spreadsheet_df(spreadsheet_file_name)
    gene_select_list = read_a_list_file(gene_list_file_name)

    result_df = select_genes_df(spreadsheet_df, gene_select_list)

    transform_name = "select_genes"
    write_transform_df(result_df, spreadsheet_file_name, transform_name, results_directory)


def select_genes_df(spreadsheet_df, gene_select_list):
    """ Subset genes based on given gene set. Output is a spreadsheet with fewer rows

    Args:
        spreadsheet_df:             genes x samples data frame
        gene_select_list:           list of some gene names in the spreadsheet

    Returns:
        spreadsheet_intersected_df: data frame with only the genes in the intersection of input gene names.
    """
    gene_names = kn.extract_spreadsheet_gene_names(spreadsheet_df)
    intersection_names = kn.find_common_node_names(gene_names, gene_select_list)
    return spreadsheet_df.loc[intersection_names]


def run_merge_df(run_parameters):
    """ Merge two phenotype matrices that correspond to same columns  (Union)

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_1_file_name", "spreadsheet_2_file_name"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_1_file_name = run_parameters['spreadsheet_1_file_name']
    spreadsheet_2_file_name = run_parameters['spreadsheet_2_file_name']

    spreadsheet_1_df = kn.get_spreadsheet_df(spreadsheet_1_file_name)
    spreadsheet_2_df = kn.get_spreadsheet_df(spreadsheet_2_file_name)

    result_df = merge_df(spreadsheet_1_df, spreadsheet_2_df)
    transform_name = "merge"
    write_transform_df(result_df, spreadsheet_1_file_name, transform_name, results_directory)


def merge_df(spreadsheet_1_df, spreadsheet_2_df):
    """ Merge two phenotype matrices that correspond to same columns (Union)

    Args:
        spreadsheet_1_df:      samples x phenotypes dataframe (spreadsheet_1_df = kn.get_spreadsheet_df(spreadsheet_filename_1))
        spreadsheet_2_df:      samples x phenotypes dataframe

    Returns:
        merged_df:     samples x phenotypes with all rows and sample names in both inputs
    """
    merged_df = pd.concat([spreadsheet_1_df, spreadsheet_2_df], axis=1)
    return merged_df


# Given expression spreadsheet and a group-samples-by criterion, create centroid of each group as a signature.
def run_cluster_statistics_df(run_parameters):
    """ Given expression spreadsheet and a group-samples-by criterion, create centroid of each group as a signature.
        Dataframe of averages for each category in a genes x samples dataframe with a samples classification dictionary.

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name", "sample_labels_file_name", "centroid_statistic"
    """
    centroid_statistic = run_parameters['centroid_statistic']
    results_directory = run_parameters['results_directory']
    spreadsheet_file_name = run_parameters['spreadsheet_file_name']
    sample_labels_file_name = run_parameters['sample_labels_file_name']

    spreadsheet_df = kn.get_spreadsheet_df(spreadsheet_file_name)
    cluster_labels_df = pd.read_csv(sample_labels_file_name, index_col=0, sep='\t', names=['sample','cluster_number'])

    result_df = cluster_statistics_df(spreadsheet_df, cluster_labels_df, centroid_statistic)

    transform_name = "cluster_" + centroid_statistic
    write_transform_df(result_df, spreadsheet_file_name, transform_name, results_directory)


def cluster_statistics_df(spreadsheet_df, labels_df, centroid_statistic='mean', axis=1):
    """ Given expression spreadsheet and a group-samples-by criterion, create centroid of each group as a signature.
        Dataframe of averages for each category in a genes x samples dataframe with a samples classification dictionary.

    Args:
        spreadsheet_df:     a genes x samples dataframe
        labels_df:          a samples classification dictionary
        centroid_statistic: ["mean", "median", "std"]
        axis:               0 = rows, 1 = columns

    Returns:
        cluster_ave_df:   a dataframe of averages for each category
    """
    labels_dict = labels_df.to_dict()['cluster_number']
    clusters_dict = {c: [] for c in list(np.unique(list(labels_dict.values())))}
    for k, v in labels_dict.items():
        clusters_dict[v].append(k)
    cluster_numbers = list(np.unique(list(labels_dict.values())))
    # labels = list(labels_dict.values())
    if centroid_statistic == 'std':
        cluster_ave_df = pd.DataFrame({i: spreadsheet_df.loc[:, clusters_dict[i]].std(axis=axis) for i in cluster_numbers})
    elif centroid_statistic == 'median':
        cluster_ave_df = pd.DataFrame({i: spreadsheet_df.loc[:, clusters_dict[i]].median(axis=axis) for i in cluster_numbers})
    else:
        cluster_ave_df = pd.DataFrame({i: spreadsheet_df.loc[:, clusters_dict[i]].mean(axis=axis) for i in cluster_numbers})

    return cluster_ave_df


def run_transpose(run_parameters):
    """ transpose a spreadsheet.

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_name_full_path = run_parameters['spreadsheet_name_full_path']

    spreadsheet_T_df = transpose_df(kn.get_spreadsheet_df(spreadsheet_name_full_path))

    transform_name = "transpose"
    write_transform_df(spreadsheet_T_df, spreadsheet_name_full_path, transform_name, results_directory)


def transpose_df(spreadsheet_df):
    """ Basic transformation dataframe to dataframe: transpose of input spreadsheet.

    Args:
        spreadsheet_df: normal orientation is genes (features aka rows) X samples (columns).

    Returns:
        transpose_df:   input orientation transposed without change of data values, i.e.
                        genes x samples transposed is samples x genes.
    """
    transpose_df = spreadsheet_df.copy()
    return transpose_df.transpose()


def run_spreadsheet_numerical_transform(run_parameters):
    """ numerical transformation of dataframe

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name", "numeric_function", (with corresponding options):
                    (z_transform_axis, z_transform_ddof)
                    (log_transform_log_base, log_transform_log_offset_
                    (threshold_cut_off, threshold_substitution_value, threshold_scope)
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_name_full_path = run_parameters['spreadsheet_name_full_path']
    numeric_function = run_parameters['numeric_function']

    spreadsheet_df = kn.get_spreadsheet_df(spreadsheet_name_full_path)

    if numeric_function == 'abs':
        spreadsheet_df = abs_df(spreadsheet_df)
        transform_name = "absolute_value"

    elif numeric_function == 'z_transform':
        z_transform_axis = run_parameters['z_transform_axis']
        z_transform_ddof = run_parameters['z_transform_ddof']
        spreadsheet_df = z_transform_df(spreadsheet_df, axis=z_transform_axis, ddof=z_transform_ddof)
        transform_name = 'z_transform'

    elif numeric_function == 'log_transform':
        log_transform_log_base = run_parameters['log_transform_log_base']
        if log_transform_log_base == "e":
            log_transform_log_base = np.exp(1)
        log_transform_log_offset = run_parameters['log_transform_log_offset']
        spreadsheet_df = log_transform_df(spreadsheet_df,
                                          log_base=log_transform_log_base,
                                          log_offset=log_transform_log_offset)
        transform_name = 'log_transform'

    elif numeric_function == 'threshold':
        threshold_cut_off = run_parameters['threshold_cut_off']
        threshold_substitution_value = run_parameters['threshold_substitution_value']
        threshold_scope = run_parameters['threshold_scope']
        spreadsheet_df = threshold_df(spreadsheet_df,
                                      cut_off=threshold_cut_off,
                                      sub_val=threshold_substitution_value,
                                      scope=threshold_scope)
        transform_name = 'threshold'

    else:
        return

    write_transform_df(spreadsheet_df, spreadsheet_name_full_path, transform_name, results_directory)


def abs_df(spreadsheet_df):
    """ Basic transformation dataframe to dataframe: absolute value of input spreadsheet.

    Args:
        spreadsheet_df: normal orientation is genes (features aka rows) X samples (columns).

    Returns:
        abs_df:         same rows and columns with magnitude of all values.
    """
    abs_df = spreadsheet_df.copy()
    return abs_df.abs()


def z_transform_df(spreadsheet_df, axis=1, ddof=0):
    """ Basic transformation dataframe to dataframe: zscore by rows for genes x samples dataframe.

    Args:
        spreadsheet_df: normal orientation is genes (features aka rows) X samples (columns).
        scope:          0 = by rows, 1 = by columns

    Returns:
        z_transform_df:
    """
    z_transform_df = spreadsheet_df.copy()
    z_transform_df.data = stats.zscore(z_transform_df.as_matrix(), axis=axis, ddof=ddof)
    return z_transform_df


def log_transform_df(spreadsheet_df, log_base=np.exp(1), log_offset=0):
    """ Basic transformation dataframe to dataframe: log of input spreadsheet

    Args:
        spreadsheet_df:

    Returns:
        log_transform_df:
    """
    log_transform_df = spreadsheet_df.copy()
    log_transform_df.data = log_offset + np.log(log_transform_df.as_matrix()) / np.log(log_base)
    return log_transform_df


def threshold_df(spreadsheet_df, cut_off, sub_val=0, scope='SUB_BELOW'):
    """ Basic transformation dataframe to dataframe: threshold replacement of input spreadsheet
    Args:
        spreadsheet_df:  normal orientation is genes (features aka rows) X samples (columns).
    Returns:
        threshold_df:
    """
    threshold_df = spreadsheet_df.copy()
    d = threshold_df.as_matrix()
    if scope == 'SUB_BELOW':
        d[d <= cut_off] = sub_val
    else:
        d[d >= cut_off] = sub_val
    threshold_df.data = d
    return threshold_df


def run_stats_df(run_parameters):
    """ get statistic for a dataframe

    Args:           run_parameters with keys:
                    "results_directory", "spreadsheet_file_name", "stats_function", "direction_reference"
    """
    results_directory = run_parameters['results_directory']
    spreadsheet_file_name = run_parameters['spreadsheet_file_name']
    stats_function = run_parameters['stats_function']
    direction_reference = run_parameters['direction_reference']

    spreadsheet_df = kn.get_spreadsheet_df(spreadsheet_file_name)
    result_df = stats_df(spreadsheet_df, stats_function=stats_function, direction_reference=direction_reference)

    transform_name = stats_function + '_' + direction_reference
    write_transform_df(result_df, spreadsheet_file_name, transform_name, results_directory)


def stats_df(spreadsheet_df, stats_function='sum', direction_reference='columns'):
    """  Basic statistic of input spreadsheet

    Args:
        spreadsheet_df:       normal orientation is genes (features aka rows) X samples (columns).
        stats_function:       one of ['min', 'max', 'mean', 'median', 'variation', 'std_deviation', 'sum']
        direction_reference:  one of ['columns', 'rows', 'all']

    Returns:
        spreadsheet_df:       dataframe with requested statistic in requested direction
    """
    in_df = spreadsheet_df.copy()
    def ret_sum():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.sum(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.sum(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            s = in_df.sum().sum()
            out_df = pd.DataFrame(data=s, index=[stats_function], columns=[stats_function])
            return out_df

    def ret_max():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.max(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.max(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            m = in_df.max().max()
            out_df = pd.DataFrame(data=m, index=[stats_function], columns=[stats_function])
            return out_df

    def ret_min():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.min(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.min(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            m = in_df.min().min()
            out_df = pd.DataFrame(data=m, index=[stats_function], columns=[stats_function])
            return out_df

    def ret_mean():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.mean(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.mean(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            out_df = pd.DataFrame(data=np.mean(in_df.as_matrix()), index=[stats_function], columns=[stats_function])
            return out_df

    def ret_median():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.median(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.median(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            out_df = pd.DataFrame(data=np.median(in_df.as_matrix()), index=[stats_function], columns=[stats_function])
            return out_df

    def ret_variation():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.var(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.var(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            out_df = pd.DataFrame(data=np.var(in_df.as_matrix()), index=[stats_function], columns=[stats_function])
            return out_df

    def ret_std_dev():
        if direction_reference == 'columns':
            out_df = pd.DataFrame(in_df.std(axis=0)).transpose()
            out_df.index = [stats_function]
            return out_df
        elif direction_reference == 'rows':
            out_df = pd.DataFrame(in_df.std(axis=1))
            out_df.columns = [stats_function]
            return out_df
        else:
            out_df = pd.DataFrame(data=np.std(in_df.as_matrix()), index=[stats_function], columns=[stats_function])
            return out_df

    stats_function_options = {
        'sum': ret_sum
        , 'max': ret_max
        , 'min': ret_min
        , 'mean': ret_mean
        , 'median': ret_median
        , 'variation': ret_variation
        , 'std_deviation': ret_std_dev}

    return stats_function_options[stats_function]()


def write_transform_df(spreadsheet_df, spreadsheet_file_name, transform_name, results_directory):
    """ Assemble the file name and write the spreadsheet.

    Args:
        spreadsheet_df:         dataframe
        spreadsheet_file_name:  the base filename of the spreadsheet_df before transformation
        transform_name:         the name to append after the spreadsheet_file_name
        results_directory:      an existing directory to write to
    """
    result_name = get_outfile_name(results_directory, spreadsheet_file_name, transform_name)
    spreadsheet_df.index.name = None
    spreadsheet_df.to_csv(result_name, sep='\t',float_format='%g')


def get_outfile_name(destination_dir, spreadsheet_file_name, transform_name, file_ext='tsv', timestamp=True):
    """ construct a full path output file name from destination path, spreadsheet file name,
        transformation name and file extenstion

     Args:
         destination_dir:                   where the file will be written (must already exists)
         spreadsheet_file_name:             usually the input file name (before transformation)
         transform_name:                    the operation performed on the input file
         file_ext:                          default is '.tsv'

    Returns:
        spreadsheet_transformed_file_name:  full path output file name
    """
    nix_dir, name_base = os.path.split(spreadsheet_file_name)
    name_base, nix_ext = os.path.splitext(name_base)
    name_base = name_base + '_' + transform_name
    if timestamp == True:
        name_base = kn.create_timestamped_filename(name_base, file_ext)
    else:
        name_base = name_base + '.' + file_ext

    return os.path.join(destination_dir, name_base)


def read_a_list_file(input_file_name):
    """ Read a text file into a python list.

    Args:
        input_file_name:     full path name of a file containing a list

    Returns:
        a list that is contained in the file
    """
    with open(input_file_name, 'r') as fh:
        str_input = fh.read()
    return list(str_input.split())
