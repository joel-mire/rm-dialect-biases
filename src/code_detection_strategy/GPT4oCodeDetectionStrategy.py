
from openai import OpenAI
import os
from tqdm import tqdm
from code_detection_strategy.CodeDetectionStrategy import CodeDetectionStrategy
from constants import *
import pandas as pd
from utils.pandas_utils import save_df

class GPT4oCodeDetectionStrategy(CodeDetectionStrategy):
  def __init__(self):
    self.client = OpenAI()
    self.result_col = GPT4O_CODE_PREDICTION_COL

  def contains_code(self, text):
    messages = [{
      "role": "user",
      "content": "Does the following text contain any code (e.g., Python, Java, Javascript, Go, Rust, LaTex)? Answer 'yes' or 'no'.\n\n" + text
    }]
    response = self.client.chat.completions.create(
      model=GPT4O_VERSION,
      messages=messages,
      temperature=0,
      top_p=1
    )
    return response.choices[0].message.content.strip().lower() == 'yes'
  
  def detect(self, df, results_path, cols):
    if os.path.exists(results_path):
      results_df = pd.read_csv(results_path)
      df[self.result_col] = results_df[self.result_col]
    else:
      code_statuses = []
      for i, row in tqdm(df.iterrows()):
        code_status = False
        for col in cols:
          if self.contains_code(row[col]):
            code_status = True
            break
        code_statuses.append(code_status)
      df[self.result_col] = code_statuses
      results_df = df[[*cols, self.result_col]]
      save_df(results_df, results_path)
    return df
