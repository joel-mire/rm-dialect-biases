import sys
sys.path.append("/home/jmire/PhonATe")   # manually set to PhonATe dir path
from phonate import AALPhonate
import pandas as pd
import argparse

def save_df(df, path):
  df.to_csv(path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--df_path", 
                        type=str,
                        required=True)
    parser.add_argument("--base_col",
                        type=str, required=True, help="Column name of the input texts")
    parser.add_argument("--mod_col", 
                        type=str,
                        required=True)
    args = parser.parse_args()

    aal_phonate = AALPhonate(config = '/home/jmire/PhonATe/phonate/default_config.json')

    df = pd.read_csv(args.df_path)

    print('Translating col:', args.base_col)
    phon_trans, phon_aug, paug_out, clean_out = aal_phonate.full_phon_aug(df[args.base_col].to_list())
    df[args.mod_col] = clean_out
    save_df(df, args.df_path)
    