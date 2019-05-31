import re
import unicodedata
from autocorrect import spell
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import os

from pattern.text import es


finalVector = []


"""
def decode_unicode_chars(words):
    return unicodedata.normalize('NFD', words).encode('ascii', 'ignore')
"""

#------------------------------------------------------------------------------------------------------------

def decode_non_ascii(words):
    """Decode non-ASCII characters from a list of tokenized words"""
    new_words = []
    for w in words:
        nw = unicodedata.normalize('NFD', w).encode('ascii', 'ignore')
        new_words.append(nw)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from a list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def remove_stopwords(words):
    """Remove stopwords from a list of tokenized words"""
    stops = set(stopwords.words('english'))
    # words=word_tokenize(sentence)
    filtered_sentence = []
    for w in words:
        if w not in stops:
            filtered_sentence.append(w)
    return filtered_sentence


def stem_words(words):
    """Stem words from a list of tokenized words"""
    stemmer = PorterStemmer()
    list_words = []
    for word in words:
        stem = stemmer.stem(word)
        list_words.append(stem)
    return list_words


def lemmatize_verbs(words):
    """Lemmatize verbs from a list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    new_words = []
    for word in words:
        new_word = lemmatizer.lemmatize(word, pos='v')
        # print(new_word)
        new_words.append(new_word)
        # print(new_words)
        # print(lemmatizer.lemmatize("cats"))
    return new_words


def normalization(words):
    #words = decode_non_ascii(words)

    words = remove_punctuation(words)
    words = remove_stopwords(words)
    #words = stem_words(words)
    words = lemmatize_verbs(words)
    return words


""" This function will be used while calling the algorithm """


def spell_correct(string):
    # words = string.split(" ")
    words = word_tokenize(string)
    correctWords = []
    for i in words:
        correctWords.append(spell(i))
    return " ".join(correctWords)

#------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------


def preprocess_training_data(filename):

    with open(filename, 'r') as f:

        alltext = f.read()
        alltext = alltext.lower()

    vector = []

    for sentence in es.parsetree(alltext, tokenize=True, lemmata=True, tags=True):

        temp = []

        for chunk in sentence.chunks:

            for word in chunk.words:

                if word.tag == 'NN' or word.tag == 'VB':

                    temp.append(word.lemma)

        vector.append(temp)



    for i in range(len(vector)):

        temp = ""
        temp = temp.join(str(vector[i]))

        words = word_tokenize(temp)

        temp = normalization(words)

        finalVector.append(temp)


#------------------------------------------------------------------------------------------------------------

def getFinalVector():

    basePath = os.path.dirname(os.path.abspath(__file__))
    targetPath = os.path.join(basePath,'AllSkills/')

    dirSkills = [os.path.join(targetPath, f) for f in os.listdir(targetPath) if os.path.isfile(os.path.join(targetPath, f))]

    for skills in dirSkills:
        preprocess_training_data(skills)


    return finalVector

#------------------------------------------------------------------------------------------------------------
'''
def reduce_dimensions_WE(Directory_GoogleNews, Directory_pca_GoogleNews):

    m1 = KeyedVectors.load_word2vec_format(Directory_GoogleNews,binary=True)

    model1 = {}

    # normalize vectors

    for string in m1.wv.vocab:

        model1[string]=m1.wv[string] / np.linalg.norm(m1.wv[string])

    # reduce dimensionality

    pca = decomposition.PCA(n_components=200)

    pca.fit(np.array(list(model1.values())))

    model1=pca.transform(np.array(list(model1.values())))

    i = 0

    for key, value in model1.items():

        model1[key] = model1[i] / np.linalg.norm(model1[i])

        i = i + 1

    d = klepto.archives.dir_archive(Directory_pca_GoogleNews, cached = True, serialized = True)

    d['big1 ']


something = reduce_dimensions_WE("/home/anuj/data/PreTrainedModel/GoogleNews-vectors-negative300.bin","/home/anuj/data/PreTrainedModel/somefile.pickle")'''
