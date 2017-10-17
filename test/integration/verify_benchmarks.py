"""
sobh@illinois.edu

"""

import filecmp
import os
import time

verification_dir = '../data/verification/'
results_dir = '../test/run_dir/results'


def verify_benchmark(algo_name, BENCHMARK_name_list, BENCHMARK_YML):
    run_command = 'python3 ../src/mini_pipelines.py -run_directory ./run_dir -run_file ' + BENCHMARK_YML
    os.system(run_command)

    All_files_in_results_dir = os.listdir(results_dir)

    num_failed_tests = 0
    num_succeed_tests = 0
    for f in All_files_in_results_dir:
        for BENCHMARK_name in BENCHMARK_name_list:
            if BENCHMARK_name in f:
                RESULT = os.path.join(results_dir, f)
                BENCHMARK = os.path.join(verification_dir, BENCHMARK_name + '.tsv')
                if filecmp.cmp(RESULT, BENCHMARK) == True:
                    num_succeed_tests += 1
                    print(BENCHMARK, '______ PASS ______')
                else:
                    num_failed_tests += 1
                    print(BENCHMARK, '****** FAIL ******')
    return num_succeed_tests, num_failed_tests


def main():
    BENCHMARK = {'spreadsheet_transpose' : ['TEST_1_transpose.yml', 'spreadsheet_One_transpose'],
                 'spreadsheets_common_samples' : ['TEST_2_common_samples.yml',
                                                  'spreadsheet_One_common_samples',
                                                  'spreadsheet_Two_common_samples'],
                 'spreadsheets_merge' : ['TEST_3_merge.yml',
                                         'spreadsheet_One_merge'],
                 'select_spreadsheet_genes' : ['TEST_4_select_genes.yml', 'gene_samples_1_select_genes'],
                 'spreadsheet_clustering_averages' : ['TEST_5_cluster_averages.yml',
                                                          'gene_samples_small_cluster_median'],
                 'spreadsheet_select_pheno_categorical' : ['TEST_6_select_categorical.yml',
                                                           'tcga_ucec_somatic_mutation_data_phenotype_category',
                                                           'UCEC_phenotype_phenotype_category'],
                 'numerical_tranform' : ['TEST_7_numerical_transform.yml', 'spreadsheet_A_.G_absolute_value'],
                 'stat_values' : ['TEST_8_stat_value.yml', 'gene_samples_1_sum_columns']
                 }

    os.system('make env_setup')
    start_time = time.time()
    total_success, total_failure = 0, 0
    for key in BENCHMARK.keys():
        BENCHMARK_list = BENCHMARK[key]
        BENCHMARK_YML = BENCHMARK_list[0]
        print()
        print("INFO: Running test ", "./run_dir/" + BENCHMARK_YML)
        num_succeed_tests, num_failed_tests = verify_benchmark(key, BENCHMARK_list[1:], BENCHMARK_YML)
        total_success += num_succeed_tests
        total_failure += num_failed_tests
        os.system('rm ./run_dir/results/*')
    end_time = time.time()
    print()
    print("Ran {} tests in {}s".format(total_success + total_failure, end_time - start_time))
    if (total_failure == 0):
        print("OK")
        print()
    else:
        print("FAILED(errors={})".format(total_failure))


if __name__ == "__main__":
    main()
