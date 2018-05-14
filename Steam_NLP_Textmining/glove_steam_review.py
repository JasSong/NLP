import csv
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from pprint import pprint
import operator
import glove
from scipy.spatial.distance import cosine
import pickle


def read_data(path,encoding ='utf16'):
    raw_data = []
    with open(path, 'r',encoding=encoding) as f:
        a = csv.reader(f)
        for i in a:
            raw_data.append(i[0])
    
    return raw_data

def mk_co_mtx_dic(data, min_df = 10, ngram_range=(1,1)):
    vectorizer = CountVectorizer(min_df=min_df, ngram_range = ngram_range)

    X = vectorizer.fit_transform(data)
    Xc = X.T * X
    Xc.setdiag(0)
#     print(Xc.setdiag(0))
    result = Xc.toarray()
    dic ={}
    for idx1, word1 in enumerate(result):
        tmpdic={}
        for idx2, word2 in enumerate(word1):
            if word2 > 0 :
                tmpdic[idx2] = word2
        dic[idx1] = tmpdic

    return dic

def voc_list(data, min_df = 10, ngram_range=(1,1)) :
    vectorizer = CountVectorizer(min_df=min_df, ngram_range = ngram_range)

    X = vectorizer.fit_transform(data)
    
    vocab = sorted(vectorizer.vocabulary_.items(), key = operator.itemgetter(1))
    vocab = [word[0] for word in vocab]
    # print(vocab)
    return vocab

def train_glove(dic_comtx, dimension = 100, alpha = 0.75, x_max = 100.0, epoch = 20, batch = 200):
    model = glove.Glove(dic_comtx, d = dimension, alpha = alpha, x_max = x_max)
    for epoch in range(epoch):
        err = model.train(batch_size = batch, workers = 4)
        print("epoch %d, error %.3f" % (epoch, err), flush=True)
    
    wordvectors = model.W #extract wordvector
    
    return wordvectors

def most_similar(word, vocab, vecs, topn=10): #use cosine similiarity
    query = vecs[vocab.index(word)]
    result = []
    for idx, vec in enumerate(vecs):
	    if idx is not vocab.index(word):
		    result.append((vocab[idx],round(1-cosine(query,vec),5)))
    result = sorted(result,key=lambda x: x[1],reverse=True)

    return result[:topn]


if __name__ == '__main__':
    #read data
    data = read_data('data_preprocessed_sample_final.txt')

    #make co-occurence matrix
    co_dic = mk_co_mtx_dic(data)

    # voca list
    voca = voc_list(data)

    #training and make_wordvectors
    wordvectors = train_glove(co_dic, dimension=100, batch = 200)

    with open('glove.pickle', 'wb') as f:
        pickle.dump([voca,wordvectors],f)

    #evaluation by cosine similarity
    # whole_voca_sim_list = {}
    # for v in voca :
    #     whole_voca_sim_list[v] = most_similar(word=v, vocab = voca, vecs = wordvectors, topn = 20)

    # with open('noun.txt','rb', encoding = 'utf16') as f:
    #     c = csv.DictReader(f,fieldnames =('tag','count'))
    #     for i in c['tag']:
    #         print(i)

    spec_voca = ['game','play','time','story','feel','first','find','love','buy','need','recommend','character','new','hours','level','sound','design','effect','action','item']
    for v in spec_voca:
        sim = most_similar(word = v, vocab = voca, vecs = wordvectors, topn = 10)
        print(sim)
    #vocabulary 이외 단어를 대입했을때 유사도
    # most_simlilar(word='word', vocab = voca, vecs = wordvectors, topn = 20)

    with open('abc.txt', w,encoding='utf16') as f:

    pprint('finished!')
