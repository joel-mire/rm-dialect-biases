import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, ttest_rel, pearsonr, spearmanr
from statsmodels.stats.multitest import multipletests

def ttestSummaries(df,condition_col,measure_cols,paired=None,fillna=None):
  """Function that compares a set of features in two groups.
  df: data containing measures and conditions
  condition_col: column name containing the group belonging (e.g., control vs. treatment)
  measure_cols: column names to compare accross groups (e.g., num words, num pronouns, etc)
  paired: None if indep. t-test, else: name of column to pair measures on.
  """
  d = {}
  
  if paired:
    df = df.loc[~df[paired].isnull()]
    df = df.sort_values(by=[paired,condition_col])
    
  for m in measure_cols:
    d[m] = ttestSummary(df,condition_col,m,paired=paired,fillna=fillna)
    
  statDf = pd.DataFrame(d).T
  statDf["p_holm"] = multipletests(statDf["p"],method="h")[1]
  return statDf

def ttestSummary(df,condition_col,measure_col,paired=None,fillna=None):
  # conds = sorted(list(df[condition_col].unique()))
  conds = sorted(filter(lambda x: not pd.isnull(x),df[condition_col].unique()))

  conds = conds[:2]
  assert len(conds) == 2, "Not supported for more than 2 conditions "+str(conds)
  
  a = conds[0]
  b = conds[1]
  df = df[df[condition_col].isin([a,b])]

  if paired:
    # merge and remove items that don't have two pairs
    pairs = df.groupby(by=paired)[measure_col]
    pair_counts = pairs.count()
    
    if fillna is not None:
      pair_ids = pair_counts[pair_counts >= 1].index
      df.loc[df[paired].isin(pair_ids),measure_col] = df.loc[df[paired].isin(pair_ids),measure_col].fillna(0)
    else:
      pair_ids = pair_counts[pair_counts == 2].index
    
    ix = df[paired].isin(pair_ids)
  else:
    ix = ~df[measure_col].isnull()
    
  s_a = df.loc[(df[condition_col] == a) & ix,measure_col]
  s_b = df.loc[(df[condition_col] == b) & ix,measure_col]

  out = ttestAndCohensD(s_a,s_b,a,b,paired=paired)
  
  return out

def ttestAndCohensD(s_a,s_b,a,b,paired=False):
  out = {
    f"mean_{a}": s_a.mean(),
    f"mean_{b}": s_b.mean(),
    f"std_{a}": s_a.std(),
    f"std_{b}": s_b.std(),
    f"n_{a}": len(s_a),
    f"n_{b}": len(s_b),    
  }
  if paired:    
    t, p = ttest_rel(s_a,s_b)
  else:
    t, p = ttest_ind(s_a,s_b)
    
  out["t"] = t
  out["p"] = p

  # Cohen's d  
  out["d"] = (s_a.mean() - s_b.mean()) / (np.sqrt(( s_a.std() ** 2 + s_b.std() ** 2) / 2))
  return out

def correlSummaries(df,left,rights,method="pearsonr"):
  d = {}
  for c in rights:
    d[c] = correlSummary(df,left,c,method=method)

  statDf = pd.DataFrame(d).T
  statDf["p_holm"] = multipletests(statDf["p"],method="h")[1]
  
  return statDf


def correlSummary(df,left,right,method="pearsonr"):
  # df[left] = pd.to_numeric(df[left], errors='coerce')
  # df[right] = pd.to_numeric(df[right], errors='coerce')
  corrF = spearmanr if method == "spearmanr" else pearsonr
  ix = ~(df[left].isnull() | df[right].isnull() )
  d = df[ix]
  r,p = corrF(d[left],d[right])
  n = len(d)
  return {"n":n,"r":r,"p":p}