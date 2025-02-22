from translation_strategy.TranslationStrategy import TranslationStrategy
from constants import *
from utils.pandas_utils import save_df, convert_col_name_base_to_mod
import pandas as pd
import os
import pandas as pd
from tqdm import tqdm
tqdm.pandas()


class ValueTranslationStrategy(TranslationStrategy):

  def translate(self, df, df_name, input_cols, output_col_suffixes, force_retranslate):
    translations_path = f'{TRANSLATIONS_DIR}/value/{df_name}.csv'
    if not os.path.exists(translations_path):
      translations_df = df[input_cols]
      save_df(translations_df, translations_path)
    else:
      translations_df = pd.read_csv(translations_path)

    translation_pairs = []
    for input_col in input_cols:
      for output_col_suffix in output_col_suffixes:
        translation_pairs.append((input_col, convert_col_name_base_to_mod(input_col, output_col_suffix)))
    base_cols = [base_col for base_col, mod_col in translation_pairs]
    mod_cols = [mod_col for base_col, mod_col in translation_pairs]
    if not all(col in translations_df.columns for col in mod_cols) or force_retranslate:
        base_cols_str = ' '.join(base_cols)
        mod_cols_str = ' '.join(mod_cols)
        command = f"python {VALUE_SCRIPT_PATH} --df_path={translations_path} --base_cols {base_cols_str} --mod_cols {mod_cols_str}"
        error_message = f"""Missing VALUE translations. 
        Check out the VALUE repo (https://github.com/SALT-NLP/value) then follow its README instructions for installing dependencies. 
        Then run the following command from the VALUE project root after activating the value conda env: {command}"""
        raise RuntimeError(error_message)

    translations_df = pd.read_csv(translations_path)
    for mod_col in mod_cols:
      df[mod_col] = translations_df[mod_col]
    return df
