from abc import ABC, abstractmethod

class CodeDetectionStrategy(ABC):

  @abstractmethod
  def detect(self, df_path):
    pass