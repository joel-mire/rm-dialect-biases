import pandas as pd
from tqdm import tqdm
from constants import *
import argparse
import sys
from src.Dialects import AfricanAmericanVernacular
sys.path.append(VALUE_ROOT_DIR)
tqdm.pandas()

def save_df(df, path):
  df.to_csv(path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--df_path", 
                        type=str,
                        required=True)
    parser.add_argument("--base_cols", 
                        nargs='+', 
                        type=str,
                        required=True)
    parser.add_argument("--mod_cols", 
                        nargs='+', 
                        type=str,
                        required=True)
    args = parser.parse_args()

    dialect = AfricanAmericanVernacular(lexical_swaps={}, 
                                        morphosyntax=True)
    
    df = pd.read_csv(args.df_path)


    for base_col, mod_col in zip(args.base_cols, args.mod_cols):
        print('Translating col:', base_col)

        results = []
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Processing {base_col}"):
            converted_value = dialect.convert_sae_to_dialect(row[base_col])
            results.append(converted_value)
        
        df[mod_col] = results
        
        save_df(df, args.df_path)