import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import sys
from constants import *
sys.path.append(USER_HOME_DIR)

def idp(counts_df, col_name):
    """Calculates word association metrics using the method from Monroe et al. (2008).

    Args:
        counts_df (pd.DataFrame): DataFrame with word counts in each category.
        col_name (str): The name of the target category.

    Returns:
        pd.Series: A Series with words as indices and association scores as values.
    """
    counts = counts_df.copy()
    counts["all"] = counts.sum(axis=1)
    not_col_name = "not_col_name"
    counts[not_col_name] = counts[counts.columns.drop(["all", col_name])].sum(axis=1)
    sums = counts.sum(axis=0)

    f_col_name = sums[col_name] / sums['all']
    f_not_col_name = 1 - sums[col_name] / sums['all']

    numerator_col = counts[col_name] + f_col_name * counts['all']
    denominator_col = (sums[col_name] + f_col_name * sums['all']) - counts[col_name] + f_col_name * counts['all']
    l_col_name = numerator_col / denominator_col

    numerator_not_col = counts[not_col_name] + f_not_col_name * counts['all']
    denominator_not_col = (sums[not_col_name] + f_not_col_name * sums['all']) - counts[not_col_name] + f_not_col_name * counts['all']
    l_not_col_name = numerator_not_col / denominator_not_col

    sigma = np.sqrt(1.0 / numerator_col + 1.0 / numerator_not_col)
    delta = (np.log(l_col_name) - np.log(l_not_col_name)) / sigma

    return delta

def fit_vectorizer(text, vec_kwargs=None):
    """Fits a CountVectorizer to the provided text.

    Args:
        text (List[str]): List of text documents.
        vec_kwargs (dict, optional): Keyword arguments for CountVectorizer.

    Returns:
        CountVectorizer: The fitted vectorizer.
    """
    if vec_kwargs is None:
        vec_kwargs = {
            "min_df": 0.005,
            "ngram_range": (1, 1),
            # "stop_words": "english"
        }
    vec = CountVectorizer(**vec_kwargs)
    vec.fit(text)
    return vec

def create_vocab_df(data_dict, return_vectorizer=False, vec_kwargs=None):
    """Creates a vocabulary DataFrame with word counts for each category.

    Args:
        data_dict (Dict[str, List[str]]): Dictionary with category names as keys and lists of texts as values.
        return_vectorizer (bool, optional): If True, returns the vectorizer along with the DataFrame.
        vec_kwargs (dict, optional): Keyword arguments for CountVectorizer.

    Returns:
        pd.DataFrame or (pd.DataFrame, CountVectorizer): The vocabulary DataFrame, and optionally the vectorizer.
    """
    all_texts = []
    for texts in data_dict.values():
        all_texts.extend(texts)

    vec = fit_vectorizer(all_texts, vec_kwargs)
    vocab = vec.get_feature_names_out()
    vocab_df = pd.DataFrame(index=vocab)

    for category, texts in data_dict.items():
        data = vec.transform(texts)
        vocab_df[category] = np.asarray(data.sum(axis=0)).flatten()

    if return_vectorizer:
        return vocab_df.fillna(0), vec
    else:
        return vocab_df.fillna(0)

def get_alignments(data_dict, alignment_category=None, return_vectorizer=False, vec_kwargs=None):
    """Computes word alignments for the given categories.

    Args:
        data_dict (Dict[str, List[str]]): Dictionary with category names and texts.
        alignment_category (str, optional): The category to align to. If None, aligns all categories.
        return_vectorizer (bool, optional): If True, returns the vectorizer.
        vec_kwargs (dict, optional): Keyword arguments for CountVectorizer.

    Returns:
        pd.DataFrame or (pd.DataFrame, CountVectorizer): DataFrame of alignments, and optionally the vectorizer.
    """
    if return_vectorizer:
        vocab_df, vec = create_vocab_df(data_dict, return_vectorizer=True, vec_kwargs=vec_kwargs)
    else:
        vocab_df = create_vocab_df(data_dict, vec_kwargs=vec_kwargs)

    if alignment_category is None:
        alignments = {}
        for category in data_dict.keys():
            alignments[category] = idp(vocab_df, category)
        alignments_df = pd.DataFrame(alignments)
    else:
        alignments_df = pd.DataFrame({alignment_category: idp(vocab_df, alignment_category)})

    if return_vectorizer:
        return alignments_df, vec
    else:
        return alignments_df