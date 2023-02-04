import re
from nltk.tokenize import sent_tokenize


def clean_text_numbers_special_char(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


def sentence_extraction(paragraph):
    return sent_tokenize(paragraph)


def clean_string(string):
    string = string.lower()
    string = re.sub(r"\'s", " is", string)
    string = re.sub(r"\'ve", " have", string)
    string = re.sub(r"can't", "cannot", string)
    string = re.sub(r"n't", " not", string)
    string = re.sub(r"i'm", "i am", string)
    string = re.sub(r"\'re", " are", string)
    string = re.sub(r"\'d", " would", string)
    string = re.sub(r"\'ll", " will", string)
    string = re.sub(r",", " ", string)
    string = re.sub(r"\.", " ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\/", " ", string)
    string = re.sub(r"\^", " ^ ", string)
    string = re.sub(r"\+", " + ", string)
    string = re.sub(r"\-", " - ", string)
    string = re.sub(r"\=", " = ", string)
    string = re.sub(r"'", " ", string)
    string = re.sub(r"(\d+)(k)", r"\g<1>000", string)
    string = re.sub(r":", " : ", string)
    string = re.sub(r" e g ", " eg ", string)
    string = re.sub(r" b g ", " bg ", string)
    string = re.sub(r" u s ", " american ", string)
    string = re.sub(r"\0s", "0", string)
    string = re.sub(r" 9 11 ", "911", string)
    string = re.sub(r"e - mail", "email", string)
    string = re.sub(r"j k", "jk", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string
