from constants import *

def save_df(df, path):
  df.to_csv(path, index=False)

def convert_col_name_base_to_mod(base_col_name, mod_suffix):
   last_underscore_idx = base_col_name.rfind('_')
   return base_col_name[:last_underscore_idx + 1] + mod_suffix

def get_corresponding_score_col(txt_col_name, prompt_strategy, model, dataset_name):
  if dataset_name == DG_DATASET_NAME:
    candidate_type = CHOSEN_KEY
    suffix = txt_col_name.split('_')[-1]
  elif dataset_name == RB_DATASET_NAME:
    _, candidate_type_shortname, suffix = txt_col_name.split('_')
    candidate_type = CHOSEN_KEY if candidate_type_shortname == 'chos' else REJECTED_KEY
  return f'{suffix}${prompt_strategy}${model}${candidate_type}'

def get_score_col_name(model, prompt_strategy, suffix, candidate_type):
   return f'{suffix}${prompt_strategy}${model}${candidate_type}'