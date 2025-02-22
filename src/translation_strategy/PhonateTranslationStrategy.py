from translation_strategy.TranslationStrategy import TranslationStrategy
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
import queue
import pandas as pd
from constants import *
import os
from utils.pandas_utils import save_df, convert_col_name_base_to_mod

def stream_reader(pipe, queue):
    """Reads lines from a pipe and puts them into the queue."""
    for line in pipe:
        queue.put(line)

class PhonateTranslationStrategy(TranslationStrategy):

  def translate(self, df, df_name, input_cols, output_col_suffixes, force_retranslate):
    futures = []
    progress_queue = Queue()
    done_event = threading.Event()

    def print_progress(done_event):
        while not done_event.is_set() or not progress_queue.empty():
            try:
                line = progress_queue.get(timeout=0.1)
                print(line, end='')
                sys.stdout.flush()
            except queue.Empty:
                continue

    progress_thread = threading.Thread(target=print_progress, args=(done_event,))
    progress_thread.start()

    with ThreadPoolExecutor(max_workers=4) as executor:
      for input_col_name in input_cols:
        for output_col_suffix in output_col_suffixes:
            output_col_name = convert_col_name_base_to_mod(input_col_name, output_col_suffix)
            if output_col_name not in df.columns or force_retranslate:
                futures.append(
                    executor.submit(self.process_phonate, 
                                    df, 
                                    df_name,
                                    input_col_name, 
                                    output_col_name, 
                                    progress_queue)
                )
    done_event.set()
    progress_thread.join()
    return df

  def process_phonate(self,df, df_name, input_col_name, output_col_name, progress_queue):
      return self.add_phonate_col(df, df_name, input_col_name, output_col_name, progress_queue)

  def add_phonate_col(self,
                      df: pd.DataFrame, 
                      df_name: str,
                      input_col_name: str,
                      output_col_name: str,
                      progress_queue: Queue): 
      phonate_input_path = f'{TRANSLATIONS_DIR}/phonate/{df_name}_{input_col_name}.csv'
      if os.path.exists(phonate_input_path) and not FORCE_REBUILD_PHONATE:
          phonate_input_df = pd.read_csv(phonate_input_path)
          if output_col_name in phonate_input_df.columns:
              print(f"Using cached results for translation from {input_col_name} -> {output_col_name}")
              df[output_col_name] = phonate_input_df[output_col_name]
              return df

      phonate_input_df = df[[input_col_name]]
      save_df(phonate_input_df, phonate_input_path)

      command_parts = [PHONATE_PYTHON_PATH, 
                      PHONATE_SCRIPT_PATH, 
                      f'--df_path={phonate_input_path}',
                      f'--base_col={input_col_name}',
                      f'--mod_col={output_col_name}']
      
      print("Invoking...", command_parts)
      # Start the subprocess and concurrently read stdout and stderr
      with subprocess.Popen(command_parts, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True, 
                            bufsize=1, 
                            universal_newlines=True) as proc:
          with ThreadPoolExecutor(max_workers=2) as executor:
              stdout_future = executor.submit(stream_reader, proc.stdout, progress_queue)
              stderr_future = executor.submit(stream_reader, proc.stderr, progress_queue)
              stdout_future.result()
              stderr_future.result()

          # Check for errors in stderr
          stderr_output = proc.stderr.read()
          if stderr_output:
              print(f"Error occurred in subprocess: {stderr_output}")
      proc.wait()
      phonate_input_df = pd.read_csv(phonate_input_path)
      df[output_col_name] = phonate_input_df[output_col_name]
      return df