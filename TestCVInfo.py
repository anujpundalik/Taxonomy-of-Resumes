from gensim.models import Word2Vec, KeyedVectors

from pattern.text import es

import textract

from os import listdir

from os.path import isfile, join,dirname,abspath

import numpy as np

from scipy import spatial



model = Word2Vec.load("TestModel")
basePath = dirname(abspath(__file__))

document_w2v = []
w2vJob = []

def getQW2V():


    dir_cvs = join(basePath,'fileUploads/')
    dircvs = [join(dir_cvs, f) for f in listdir(dir_cvs) if isfile(join(dir_cvs, f))]


    val = True

    for cv in dircvs:

        CVData = textract.process(cv).decode('utf-8')

        w2v = []

        for sentence in es.parsetree(CVData.lower(), tokenize=True, lemmata=True, tags=True):

            for chunk in sentence.chunks:

                for word in chunk.words:

                    if val:

                        if word.lemma in model.wv.vocab:

                            w2v.append(model.wv[word.lemma])

                        else:

                            if word.lemma.lower() in model.wv.vocab:
                                w2v.append(model.wv[word.lemma.lower()])

                    else:

                        if word.string in model.keys():

                            w2v.append(model[word.string])

                        else:

                            if word.string.lower() in model.keys():
                                w2v.append(model[word.string.lower()])

        document_w2v.append((np.mean(w2v, axis=0), cv))

#-----------------------------------------------------------------------------------------------------------------------

    if val:

        filename = join(basePath,'requirements.txt')

        dataFile = open(filename)

        data = dataFile.read()

        data = data.lower()

    for sentence in es.parsetree(data, tokenize=True, lemmata=True, tags=True):

        for chunk in sentence.chunks:

            for word in chunk.words:

                if val:

                    if word.lemma in model.wv.vocab:

                        w2vJob.append(model.wv[word.lemma])

                    else:

                        if word.lemma.lower() in model.wv.vocab:

                            w2vJob.append(model.wv[word.lemma.lower()])

                else:

                    if word.string in model.keys():

                       w2vJob.append(model[word.string])

                    else:

                        if word.string.lower() in model.keys():

                            w2vJob.append(model[word.string.lower()])

    Q_w2v = np.mean(w2vJob, axis=0)

    return Q_w2v
#-----------------------------------------------------------------------------------------------------------------------


def get_filenames():

    retrieval = []
    filenames = []
    Q_w2v = getQW2V()

    for i in range(len(document_w2v)):

        retrieval.append((1 - spatial.distance.cosine(Q_w2v, document_w2v[i][0]),document_w2v[i][1]))

    retrieval.sort(reverse=True)

    for i in range(len(retrieval)):

        split_retrieval = str(retrieval[i]).split('/')
        last = split_retrieval[-1]
        filenames.append(last[:-2])

    print(filenames)
    return filenames

def generate_output():

    final_output = []
    filenames = get_filenames()

    user_details = []

    with open('userDetails.txt', 'r') as f:
        for line in f:
            user_details.append(line)


    for i in range(len(filenames)):

        for j in range(len(user_details)):

            splitline = user_details[j].split(',')
            compare_string = splitline[-1]


            if filenames[i] == compare_string[:-1]:
                final_output.append(user_details[j])
                del user_details[j]
                break


    return final_output


generate_output()