import sys
from constants import *
sys.path.append(USER_HOME_DIR)
import pandas as pd
from resources.langDialect.umass_demoens_langid import predict, twokenize
from langid.langid import LanguageIdentifier, model

dialCats = ["aav","hispanic","other","white"]
lpy_identifier = None
def load_lpy_identifier():
  """Idempotent"""
  global lpy_identifier
  if lpy_identifier is not None:
    return
  lpy_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def countDialectWords(tweet):
    if tweet is None or pd.isnull(tweet):
        return pd.Series(index=dialCats).fillna(0.0)
    else:
        toks = twokenize.tokenizeRawTweetText(tweet)
        total_words = len(toks)
        props = pd.Series(predict.predict(toks), index=dialCats)
        props = props / total_words  # Normalize by total words
        return props.fillna(0.0)

def detectDialect(text):
  s = countDialectWords(text)
  am = s[dialCats].idxmax()
  
  if s[am] >= .80:
    s["dialect_80pct"] = am
  else:
    s["dialect_80pct"] = "other"
    
  s["dialect_argmax"] = am

  return s

predict.load_model()
load_lpy_identifier()