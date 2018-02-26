SCRIPT = ../src/spreadsheets_transformation_pipelines.py
RUN_DIR = ./run_dir
RUN_FILES = ../data/run_files
RESULTS_DIR = $(RUN_DIR)/results
INPUT_DATA_DIR = ../data
UNIT_TEST_TEMP_DIR = ./unit/tmp

RMR = rm -rf
MKDIR_P = mkdir -p

# ----------------------------------------------------------------
# Benchmarks setup Section                                       -
# ----------------------------------------------------------------
env_setup: create_run_dir copy_run_files

create_run_dir:
	$(MKDIR_P) $(RESULTS_DIR) 

copy_run_files:
	cp $(RUN_FILES)/*.yml $(RUN_DIR) 

clean_dir_recursively:
	$(RMR) $(RUN_DIR)


# ----------------------------------------------------------------
# Benchmarks RUN Section                                   -
# ----------------------------------------------------------------
run_all: run_spreadsheet_transpose  run_spreadsheets_common_samples  run_spreadsheets_merge  run_select_spreadsheet_genes  run_spreadsheet_clustering_averages run_spreadsheet_select_pheno_categorical run_numerical_tranform run_stat_values
	 
run_spreadsheet_transpose:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_1_transpose.yml

run_spreadsheets_common_samples:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_2_common_samples.yml

run_spreadsheets_merge:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_3_merge.yml

run_select_spreadsheet_genes:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_4_select_genes.yml

run_spreadsheet_clustering_averages:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_5_cluster_averages.yml

run_spreadsheet_select_pheno_categorical:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_6_select_categorical.yml

run_numerical_tranform:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_7_numerical_transform.yml

run_stat_values:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_8_stat_value.yml

run_kaplan_meier:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_9_kaplan_meier.yml

run_category_binary:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_10_categorical_to_bin.yml

# ----------------------------------------------------------------
# - VERIFICATION TESTS RUN SECTION                               -
# ----------------------------------------------------------------
verification_tests:
	python3 integration/verify_benchmarks.py

# ----------------------------------------------------------------
# - UNIT TESTS RUN SECTION                                       -
# ----------------------------------------------------------------
run_benchmark_test:
	python3 $(SCRIPT) -run_directory $(RUN_DIR) -run_file TEST_1_transpose.yml

# ----------------------------------------------------------------
# - CLEAN UP SECTION                                             -
# ----------------------------------------------------------------	
unit_test_cleanup:
	$(RMR) $(UNIT_TEST_TEMP_DIR)


