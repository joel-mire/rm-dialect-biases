from abc import ABC, abstractmethod

class TranslationStrategy(ABC):

  @abstractmethod
  def translate(self, df, df_name, input_cols, output_col_suffixes, force_retranslate):
    pass