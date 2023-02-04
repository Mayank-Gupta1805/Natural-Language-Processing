import spacy, nltk

def downloadIfNotfindNLTKLibrary(library):
    try:
        nltk.data.find(library)
    except LookupError:
        nltk.download(library)

def downloadIfNotPresentSpacy(library):
    if not spacy.util.is_package(library):
        spacy.cli.download(library)


# all downloads
downloadIfNotPresentSpacy("en_core_web_lg")

downloadIfNotfindNLTKLibrary('punkt')
downloadIfNotfindNLTKLibrary('stopwords')

from nltk.corpus import stopwords

# all common modules
nlp = spacy.load("en_core_web_lg")
stop_words = set(stopwords.words('english'))
