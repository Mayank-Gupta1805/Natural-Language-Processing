from backend.constants import url_dataset, INGREDIENTS_COLUMN, RECIPE_COLUMN, PREPTIME_COLUMN, COOKTIME_COLUMN, TOTALTIME_COLUMN, INSTRUCTIONS_COLUMN, SERVING_COLUMN
from backend.similarity import get_rows_from_index
import pandas as pd
from langdetect import detect as lang_detect
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def read_pandas_df_from_url(url):
    df = pd.read_csv(url, sep=',', header=0)
    return df


def isEnglishRecipe(row):
    return lang_detect(row[INGREDIENTS_COLUMN]) == 'en'


def read_pandas_df_from_url(url):
    columns_to_read = ["TranslatedRecipeName", "TranslatedIngredients", "PrepTimeInMins", "CookTimeInMins",
                       "TotalTimeInMins", "Servings", "Cuisine", "Course", "Diet", "TranslatedInstructions"]
    df = pd.read_csv(url, encoding='utf8', usecols=columns_to_read)
    df = df[df[INGREDIENTS_COLUMN].notna()]
    df["TranslatedInstructions"] = df["TranslatedInstructions"].str.split().str.join(' ')
    #df = df[df.apply(isEnglishRecipe, axis=1)]
    df.drop_duplicates(subset=RECIPE_COLUMN,
                       keep='first', inplace=True)
    return df


data = read_pandas_df_from_url(url_dataset)


def get_columns_from_index(df, index_list, columns_to_search):
    return df.loc[index_list, columns_to_search]


def get_cell_value_from_index_and_column(df, index, column_name):
    return df.loc[index, column_name]


def get_information_from_df(all_recipes, column_to_search):
    answers = []
    for index in list(all_recipes.index):
        recipe_name = get_cell_value_from_index_and_column(
            all_recipes, index, RECIPE_COLUMN)
        column_value = get_cell_value_from_index_and_column(
            all_recipes, index, column_to_search)
        answers.append({RECIPE_COLUMN: recipe_name,
                       column_to_search: column_value})
    return answers
