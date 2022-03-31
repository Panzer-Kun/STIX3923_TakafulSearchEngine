import pandas as pd
import re
import gensim.downloader as api
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from sklearn.metrics.pairwise import cosine_similarity;
from gensim.models import Word2Vec 
from gensim.models import KeyedVectors
from gensim import models
   
class System:
    def __init__(self, debug=False):
        self.debug = debug
        self.df = pd.read_csv("https://raw.githubusercontent.com/Panzer-Kun/SearchEngine/main/AIA_TakafulCombined.csv")
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
            print("Saved glove model")

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

        
    def clean_sentence(self, sentence, stopwords=False):
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

    def calculateAnswer(self, query, question_embedding):
        max_sim = -1
        index_sim = -1
        for index, faq_embedding in enumerate(self.bow_corpus):
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

    def getAnswer(self, query):
        question = self.clean_sentence(query, stopwords=False)
        question_embedding = self.dictionary.doc2bow(question.split())

        if self.debug:
            print("\n\n", query, "\n", question_embedding)

        self.calculateAnswer(query, question_embedding)
        return query 
        
