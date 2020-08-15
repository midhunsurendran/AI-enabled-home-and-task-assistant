import nltk
import json
import random
import tensorflow
import tflearn
import numpy
import warnings
import pickle

nltk.download('punkt')
from nltk import word_tokenize, punkt

warnings.filterwarnings('ignore')

stemmer = nltk.LancasterStemmer()

with open("dataIntents.json") as datafile:
    data = json.load(datafile)
    # def trainChat():
    words = []
    label = []
    docs_tag = []
    docs = []
    questions=[]
    searchWords = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            questions.append(pattern)
            wrd = nltk.word_tokenize(pattern)
            words.extend(wrd)
            docs.append(wrd)
            docs_tag.append(intent["tag"])
            if intent["tag"] not in label:
                label.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != '?']
    words = sorted(list(set(words)))
    label = sorted(label)

    training = []
    output = []

    out_empty = [0 for _ in range(len(label))]
    for x, doc in enumerate(docs):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[label.index(docs_tag[x])] = 1
        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    with open("chatdata.pickel", "wb") as f:
        pickle.dump((words, label, training, output), f)

tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def tag_of_Words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for sw in s_words:
        for i, w in enumerate(words):
            if w == sw:
                bag[i] = 1

    return numpy.array(bag)


def chat(inp):
    # print("Start Talking")
    # while True:
    # inp = input("You: ")
    if inp.lower() == "quit":
        quit()
    result = model.predict([tag_of_Words(inp, words)])
    result_index = numpy.argmax(result)
    tag = label[result_index]
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responds = tg["responses"]
    return random.choice(responds)
