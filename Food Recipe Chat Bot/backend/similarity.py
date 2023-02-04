import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher

from backend.text_preprocessor import clean_text_numbers_special_char
from backend.constants import RECIPE_COLUMN


def cosine_sim(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]  # type: ignore


def find_similar_cosine(string, list_of_strings):
    similarities = []
    for s in list_of_strings:
        similarities.append(cosine_sim(string, s))
    return similarities


def find_cosine_similar_and_return_sorted(string, list_of_strings):
    similarities = find_similar_cosine(string, list_of_strings)
    return sorted(zip(list_of_strings, similarities), key=lambda x: x[1], reverse=True)


def find_similar(string, list_of_strings):
    similarities = [similar(string, s) for s in list_of_strings]
    return similarities


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check_common_token(string1, string2):
    string1 = string1.split()
    string2 = string2.split()
    for s1 in string1:
        for s2 in string2:
            if s1 == s2:
                return True
    return False


def get_rows_from_index(df, index_list):
    return df.loc[index_list]


def get_rows_with_common_token(df, string):
    string = clean_text_numbers_special_char(string)
    common_token_list = []
    filtered_token_list = []
    list_of_recipes = df[RECIPE_COLUMN].to_list()
    for s in list_of_recipes:
        if check_common_token(string.lower(), s.lower()):
            common_token_list.append(list_of_recipes.index(s))
            filtered_token_list.append(s)
    result = find_cosine_similar_and_return_sorted(
        string, filtered_token_list)[:10]
    index_list = []
    for i, j in result[:5]:
        index_list.append(
            list(df[RECIPE_COLUMN][df[RECIPE_COLUMN] == i].index)[0])
    return get_rows_from_index(df, index_list)


def get_index_from_list_of_list_of_strings(string, list_of_list_of_strings):
    similarities = []
    for list_of_strings in list_of_list_of_strings:
        if len(list_of_strings) == 0:
            similarities.append(0)
            continue
        similarities.append(max(find_similar(string, list_of_strings)))
    return 3 if "total" in string and "time" in string else similarities.index(max(similarities))
