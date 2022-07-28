############################################################
# IT-

import nltk
import gensim
import warnings
import os
import pickle
from glob import glob
import PyPDF2
import pyLDAvis
import langdetect

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect, DetectorFactory

from pyLDAvis import gensim_models as gensimvis

# get rid of those pesky deprecation warnings.
warnings.filterwarnings("ignore",category=DeprecationWarning)

# nltk.download('stopwords')
# check if multi-dimensional list is empty
def isListEmpty(inList):
    if isinstance(inList, list): # Is a list
        return all( map(isListEmpty, inList) )
    return False # Not a list

#
def preprocess(textstring):
    s_words = stopwords.words('english')
    s_words.extend(
        ['include', 'also', 'system', 'one', 'risk', 'test', 'computer', 'data', 'may', 'fig',
         'time', 'network', 'information', 'example', 'least', 'user', 'said', 'tag', 'set', 'scan', 'computing',
         'electronic', 'action', 'embodiments', 'base', 'ip','security','et','al','device','wherein','based', 'e','g','intensity',
         'knowledge','used','mg','patent','w','claim','composition','quic','node','graph','event','request','score',
         'context','local','first','task','control','protected','i','ieee','v','k','p','ieee','acm','using','readable', 'db'
         'herein', 'flow', 'process', 'plurality','certain','filed','disorder','certain', 'filed','use','part','number',
         'mice',  'could', 'content', 'application', 'sheet', 'associated', 'particular', 'county', 'herein', 'various',
         'described','instructions', 'optimal', 'call','access', 'connected', 'pages','results', 'configured', 'second',
         'level', 'site', 'solution','histogram','determine','value','step','determined','problem','include','within',
         'list','different', 'present','stored', 'type', 'vol','d','b','h','determining','two','includes','implemented',
         'state','activity','related','received', 'source', 'sources','additional','centroid','known','date','disclosure',
         'initial','collective','publication','u','new','method','c','input','group'])

    stops = set(s_words)

    tokens = word_tokenize(textstring.lower())
    return [token.lower() for token in tokens if token.isalpha() and token not in stops]

#
# function to extract text from PDF files
#
def pdf_extractor(pdf, corpus_list, text_list):
    '''Extract the text of pdfs and return a dictionary with
   the file name as a key, and the value being a list of the pages
   and the containing texts
    '''
    with open(pdf, 'rb') as pdf_file_obj:
        try:
            # translator = Translator(to_lang="English")
            pdf_obj = PyPDF2.PdfReader(pdf_file_obj, strict=False)

            DetectorFactory.seed = 0

            for pn in range(0, pdf_obj.numPages):
                page = pdf_obj.getPage(pn)

                text = page.extractText().lower()
                # translation = translator.translate(text)

                cleaned_list = preprocess(text)
                corpus_list.append(cleaned_list)

                text_list.append((pdf, pn))
#               print(pdf_obj.extractText())

            langText = detect(text)
            #print('File '+ pdf + ' is ' + langText)
        except Exception as exc:
            print ('PDFReader Error: ' + str(exc) +' File: '+ pdf)

    pdf_file_obj.close()
    return corpus_list, text_list


#
if __name__ == '__main__':
    #
    # build a list of the countries for patents and academic
    # for all academic papers written in English, regardless of
    # country
    sources = ['patents','academic']

    countries = [('poland','europe'),('us', 'northamerica'),('australia','oceania'),('canada','northamerica'),
                 ('china','asia'),('denmark','europe'),('finland','europe'),('germany','europe'),('greece','europe'),
                 ('india','asia'),('israel','mideast'),('italy','europe'),('japan','asia'),('korea','asia'),
                 ('liechtenstein','europe'),('russia','europe'),('singapore','asia'),('southafrica','africa'),
                 ('spain','europe'),('sweden','europe'), ('switzerland','europe'), ('turkey','europe'),
                 ('taiwan','asia'),('uk','europe')]

    # The source patent and academic files are in the 'corpus' folder.
    # and are further grouped by region (mideast, asia, etc.) and
    # country
    for source in sources:
        for country in range(len(countries)):
            # build the path to this folder
            pdf_path = 'corpus/' + source + '/' + countries[country][1] + '/' + countries[country][0] + '/*.pdf'

            # grab all of the files from this particular folder
            pdfs = glob(pdf_path)

            if len(pdfs) != 0:
                print('Country                    : '+ countries[country][0])
                print('Number of PDF source files : ' + str(len(pdfs)))
            else:
                print ('There are no files in the ' + countries[country][1] + '-' + countries[country][0]+ ' folder.' )
                continue
            corpus_list = []
            text_list = []

            # read every page of the pdf file into the
            # corpus list.
            for pdf in pdfs:

               # call the extraction function
               corpus_list, text_list = pdf_extractor(pdf, corpus_list, text_list)




            # Create a dictionary representation of the documents.
            dictionary = Dictionary(corpus_list)
            # While files were found in this folder, nothing was parsed
            # from them.  This is probably due to language issues that
            # have yet to be coded for.
            if dictionary == 0:
                print('No usable files for this country.')
                continue

            # Filter out words that occur less than 5 times
            # in the whole corpus or more than 75% of the documents.
            dictionary.filter_extremes(no_below=5, no_above=0.75)

            corpus = [dictionary.doc2bow(pdf_file) for pdf_file in corpus_list]

            if len(corpus) == 0 or isListEmpty(corpus):
                print('No usable files for this country, corpus empty.')
                print('-------------')
                continue

            print('-------------')
            pickle.dump(corpus, open('corpus.pkl', 'wb'))
            #    # Make a index to word dictionary.
            dictionary.save('dictionary.gensim')

            temp = dictionary[0]  # This is only to "load" the dictionary into memory..

            id2word = dictionary.id2token

            print('Total number of pages parsed in this corpus: %d' % len(corpus))
            print('-------------')
            print('')

            # Train the topic model
            model = LdaModel(corpus=corpus, id2word=id2word, iterations=500, num_topics=5, alpha='auto')
            model.save('model1,gensim')

            topics = model.print_topics(num_words=5)
            for topic in topics:
                print(topic)


            lda_display = gensimvis.prepare(model, corpus, dictionary)
            web_page = source + '-' + countries[country][1] + '-' + countries[country][0] + '-LDA_Visualization.html'
            pyLDAvis.save_html(lda_display, web_page )
