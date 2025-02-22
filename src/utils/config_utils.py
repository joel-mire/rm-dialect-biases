from constants import *
import os

def parse_rb_execution_config(config):
  dataset_name = config[DATASET_NAME_KEY]
  col_prefix_dict = config[COL_PREFIX_DICT_KEY]
  base_suffix = config[BASE_SUFFIX_KEY]
  mod_suffixes = config[MOD_SUFFIXES_KEY]
  all_suffixes = [base_suffix] + mod_suffixes
  prompt_strategies = config[PROMPT_STRATEGIES_KEY]
  return dataset_name, col_prefix_dict, base_suffix, mod_suffixes, all_suffixes, prompt_strategies

def have_all_datasets():
  return all(os.path.exists(path) for path in [RAW_GROENWOLD_WME_PATH, RAW_GROENWOLD_AAL_PATH, RAW_DEAS_PROMPTS_PATH, RAW_DEAS_EVAL_PATH])