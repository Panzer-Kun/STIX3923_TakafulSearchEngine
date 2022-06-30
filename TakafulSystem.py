import pandas as pd
import re
import gensim.downloader as api
import gensim
import numpy
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from sklearn.metrics.pairwise import cosine_similarity;
from gensim.models import Word2Vec 
from gensim.models import KeyedVectors
from gensim import models
   
class System:
    def __init__(self, debug=False):
        self.debug = debug
        self.df = pd.read_csv("https://raw.githubusercontent.com/Panzer-Kun/STIX3923_TakafulSearchEngine/main/AIA_TakafulCombinedLatest.csv", usecols=[0,1])
        print(self.df)
        self.df.columns = ["questions", "answers"]
        self.cleaned_sentences = self.get_cleaned_sentences(stopwords=True)
        self.cleaned_sentences_with_stopwords = self.get_cleaned_sentences()
        self.sentence_words = [[word for word in document.split()] for document in self.cleaned_sentences_with_stopwords]
        self.dictionary = corpora.Dictionary(self.sentence_words)
        self.bow_corpus = [self.dictionary.doc2bow(text) for text in self.sentence_words]
        self.glove_model = None
        self.w2v_model = None
        
        try:
            self.glove_model = gensim.models.KeyedVectors.load("./glovemodel.mod")
            print("Loaded glove model")
        except:            
            self.glove_model = api.load('glove-twitter-25')
            self.glove_model.save("./glovemodel.mod")
            print("Saved glove model")

        try:
            self.w2v_model = gensim.models.KeyedVectors.load("./w2vecmodel.mod")
            print("Loaded w2v model")    
        except:            
            self.w2v_model = api.load('word2vec-google-news-300')
            self.w2v_model.save("./w2vecmodel.mod")
            print("Saved w2v model")

        self.glove_embedding_size = len(self.glove_model['computer'])
        self.w2vec_embedding_size = len(self.w2v_model['computer'])


        if self.debug:
            print(self.cleaned_sentences)
            print(self.cleaned_sentences_with_stopwords)

            for key, value in self.dictionary.items():
                print(key, ' : ', value)
            
            for sent, embedding in zip(self.cleaned_sentences_with_stopwords, self.bow_corpus):
                print(sent)
                print(embedding)

    def getWordVec(self, word, model):
        samp = model['computer']
        vec = [0] * len(samp)

        try:
            vec = model[word]  
        except:
            vec = [0] * len(samp)

        return (vec)

    def getPhraseEmbedding(self, phrase, embeddingmodel):            
        samp = self.getWordVec('computer', embeddingmodel)
        vec = numpy.array([0] * len(samp))
        den = 0

        for word in phrase.split():
            den = den + 1
            vec = vec + numpy.array(self.getWordVec(word, embeddingmodel))

        return vec.reshape(1, -1)

    def clean_sentence(self, sentence, stopwords=False):
        print(sentence)
        sentence = sentence.lower().strip()
        sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
 
        if stopwords:
            sentence = remove_stopwords(sentence)
    
        return sentence    

    def get_cleaned_sentences(self, stopwords=False):    
        sents = self.df[["questions"]]
        cleaned_sentences = []

        for index, row in self.df.iterrows():
            cleaned = self.clean_sentence(row["questions"], stopwords)
            cleaned_sentences.append(cleaned)
        
        return cleaned_sentences

    def calculateAnswer(self, query, question_embedding, sentence_embedding):
        max_sim = -1
        index_sim = -1
        for index, faq_embedding in enumerate(sentence_embedding):
            sim = cosine_similarity(faq_embedding, question_embedding)[0][0]
            print(index, sim, self.cleaned_sentences_with_stopwords[index])
            

            if sim > max_sim:
                max_sim = sim
                index_sim = index

        if self.debug:
            print("\n")
            print("Question: ", query)
            print("\n")
            print("Retrieved: ", self.df.iloc[index_sim, 0]) 
            print(self.df.iloc[index_sim, 1]) 
               
        return {
            'query': self.df.iloc[index_sim, 0], 
            'retrieved': self.df.iloc[index_sim, 1]
        }

    def getAnswer(self, query, model='w2v'):
        question = self.clean_sentence(query)
        question_embedding = self.dictionary.doc2bow(question.split())
    
        phrase_embedding = None
        sent_embeddings = []

        # with Word2Vec Model
        if model == 'w2v':
            for sent in self.cleaned_sentences:
                sent_embeddings.append(self.getPhraseEmbedding(sent, self.w2v_model))

            phrase_embedding = self.getPhraseEmbedding(question, self.w2v_model)  

        # With Glove Model
        else:
            for sent in self.cleaned_sentences:
                sent_embeddings.append(self.getPhraseEmbedding(sent, self.glove_model))

            phrase_embedding = self.getPhraseEmbedding(question, self.glove_model)  

        
        if self.debug:
            print("\n\n", query, "\n", question_embedding)

        return self.calculateAnswer(query, phrase_embedding, sent_embeddings)
        
