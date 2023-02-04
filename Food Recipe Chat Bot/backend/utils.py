from backend.constants import total_time_questions, prep_time_questions, cook_time_questions, instruction_questions, ingredients_questions, serving_questions
from backend.similarity import get_index_from_list_of_list_of_strings, get_rows_with_common_token
from backend.setup import nlp
from backend.database import data
from backend.constants import INGREDIENTS_COLUMN, PREPTIME_COLUMN, COOKTIME_COLUMN, TOTALTIME_COLUMN, INSTRUCTIONS_COLUMN, SERVING_COLUMN

from spacy.matcher import Matcher


def _extract_recipe_name(command):
    doc = nlp(command)
    # for tok in doc:
    #     print(tok.text, "-->",tok.dep_,"-->", tok.pos_)
    pattern = [{'POS': 'PROPN', "OP": "*"}, {'POS': 'NOUN', "OP": "*"}]

    matcher = Matcher(nlp.vocab)
    matcher.add("recipe_name_matcher", [pattern])

    # gives the position of matching characters start and end.
    matches = matcher(doc)
    max_length = 0
    recipe_name = ""
    for match in matches:
        length = match[2] - match[1]
        if length > max_length:
            max_length = length
            recipe_name = doc[match[1]:match[2]].text
    return recipe_name


def get_recipes_from_commend(command):
    recipe_name = _extract_recipe_name(command)
    recipes = get_rows_with_common_token(data, recipe_name)
    return recipes, recipe_name


index_to_columns = {
    0: INGREDIENTS_COLUMN,
    1: PREPTIME_COLUMN,
    2: COOKTIME_COLUMN,
    3: TOTALTIME_COLUMN,
    4: INSTRUCTIONS_COLUMN,
    5: SERVING_COLUMN
}


def get_command_context(command):
    question_index = get_index_from_list_of_list_of_strings(
        command, [ingredients_questions, prep_time_questions, cook_time_questions, total_time_questions, instruction_questions, serving_questions])
    return index_to_columns[question_index]
