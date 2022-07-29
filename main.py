############################################################
# IT-797 Natural Language Processing
# Date:       July 29. 2022
# Subject:   Final Project
# Student:   Kelly Shaw
# EMail:     aks62069@marymount.edu
# GitHub:    https://github.com/cyberthreatgurl/cyberinteltool
#
# Description:
# This python script reads PDF files, ingests the text from them, and
# performs LDA topic modeling to produce web pages of the results.
#
#
# Details:
# This python script searches the "corpus" subfolder (in same folder as this
# main.py file) for patent and academic reporting. This reporting is in PDF
# format.  Once read in, the PyPDF2 module is used to read the ASCII strings
# from the file (if possible). Then, the stop words are pulled from the text
# before being written to a gensim module dictionary. The pyLDAvis module then
# uses the Latent Dirichelt Allocation topic modeling library to fine the
# top terms in each file.
#
# The PyPDF2, gensim, pyLDAvis, nltk libraries need to be imported.
#
# Python Version:   3.8
#
# How to run this script:
# Download patent and academic reporting in to the corpus folder.  There are subfolders for
# the region and country under the patents and academic subfolders.
#
# Notes:
# This script does not translate any language (yet).  However, support for
# this feature is planned.
#
#  - Flat (scanned in) pdf files throw an error and are skipped.
#  - There is no support (yet) to scrape PDF files from a website.
#  - Empty folders are skipped.
#
# Great websites to find these files include:
#  scholar.google.com, scholar.archive.org, and patents.google.com
#
# How to run:
# - To run this script, use Python 3.8  (at least).
# - Ensure the corpus/academic and corpus/patens subfolders are populated
#   with files of interest.
# - This program then generates an index.html file and a web page for
#   each country that shows the LDA visualization of the cyber-defense
#   and cyber-offense technologies being researched and developed.
# - You can manually tweak the "stop words" until you are happy
#   that all the extraneous words have been removed from the
#   corpus.
#
import nltk
import gensim
import warnings
import os
import pickle
import glob

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

# Build the header section of the
# output index.html page
def build_html_head():
    html_heading_text = '''
    <html>
        <head><title>Cyber Security Defense and Offense Topic Modeling</title>
        <h1>Topic Modeling of Cyber Offense/Defensive Terms</h1>
        </head>
    '''
    file = open('index.html','w')
    file.write(html_heading_text)
    file.close()

# build the body section of the
# output index.html page.
def build_html_body_frame():
    html_body_text = '''
        <body bgcolor="white">
    '''
    file = open('index.html','a')
    file.write(html_body_text)
    file.close()

def build_html_end():
    html_end_text = '''
        </body>
    </html>'''
    file = open('index.html','a')
    file.write(html_end_text)
    file.close()


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
         'initial','collective','publication','u','new','method','c','input','group','entity','strategy','file','message',
         'die','media','available','accessed','table','normal','unusual','behavior','source','thus','performance''potential',
         'beyond','robust','underlay','features','claims','rules','processing','continues','wo','events','transaction',
         'address','interface','threshold','corresponding''term','short','would','due','well','make','things','products',
         'three','function','distance','three','figure','zero','actions','take','ability','knight','rl','reward','world',
         'states','order','unit','ability','classical''made','might','year','way','carried','activities','great','become',
         'act','usually','amount','cyber','political','international','term','preference','specific','long','company',
         'legal','allow','corporate','section', 'discussion', 'investments','operation', 'program','ratings','response',
         'pp','layer','independent','polynomial'] )

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
            exc
            # log this
            #print ('PDFReader Error: ' + str(exc) +' File: '+ pdf)

    pdf_file_obj.close()
    return corpus_list, text_list


#
if __name__ == '__main__':
    #
    # build a list of the countries for patents and academic
    # for all academic papers written in English, regardless of
    # country
    sources = ['patents','academic']

    countries = [('australia','oceania'),('belarus','europe'), ('canada','northamerica'),('china','asia'),
                 ('cyprus','europe'),('czech','europe'),('denmark','europe'),('finland','europe'),
                 ('france','europe'), ('germany','europe'), ('greece','europe'),('india','asia'),
                 ('israel','mideast'),('italy','europe'),('japan','asia'),
                 ('korea','asia'),('liechtenstein','europe'),('morocco','africa'),('pakistan','asia'),
                 ('poland','europe'),('russia','europe'),('saudiarabia','mideast'),('singapore','asia'),
                 ('southafrica','africa'),('spain','europe'),('srilanka','asia'),('sweden','europe'),
                 ('slovenia','europe'), ('switzerland','europe'), ('turkey','europe'),
                 ('taiwan','asia'),('uk','europe'),('us', 'northamerica')]

    build_html_head()
    build_html_body_frame()
    # The source patent and academic files are in the 'corpus' folder.
    # and are further grouped by region (mideast, asia, etc.) and
    # country
    # the corpus folder should be in the same folder as the main.py file
    data_folder = 'corpus'
    cur_dir = os.getcwd()
    abs_path = cur_dir + '/'+ data_folder
    for country in countries:
        # build the path to this folder
        # grab all of the files from this particular folder
        pdf_path = '**/' +country[0]+'/*.pdf'

        pdfs = glob.glob(pdf_path, recursive=True)
        if len(pdfs) != 0:
            print('Country : '+ country[0])
            print('Number of ' + country[0] + ' ' + ' files : ' + str(len(pdfs)))
        else:
            print ('Their are no data files for ' + country[0] )
            print('-------------')
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
            print('Corrupt {0}  files.'.format(country[0]))
            continue

        # Filter out words that occur less than 5 times
        # in the whole corpus or more than 60% of the documents.
        dictionary.filter_extremes(no_below=5, no_above=0.50)

        corpus = [dictionary.doc2bow(pdf_file) for pdf_file in corpus_list]

        if len(corpus) == 0 or isListEmpty(corpus):
            print('No usable files for this country, corpus empty.')
            continue
        else:
            total_files_in_corpus = len(pdfs)

        pickle.dump(corpus, open('corpus.pkl', 'wb'))
        #    # Make a index to word dictionary.
        dictionary.save('dictionary.gensim')

        temp = dictionary[0]  # This is only to "load" the dictionary into memory..

        id2word = dictionary.id2token
        total_pages = len(corpus)
        print('Total number of pages parsed in this corpus: %d' % total_pages)
        print('-------------')
        print('')

        # Train the topic model
        model = LdaModel(corpus=corpus, id2word=id2word, iterations=500, num_topics=5, alpha='auto')
        model.save('model1,gensim')

        topics = model.print_topics(num_words=5)
        for topic in topics:
            print(topic)

        lda_display = gensimvis.prepare(model, corpus, dictionary)
        web_page = country[1] + '-' + country[0] + '-LDA.html'
        pyLDAvis.save_html(lda_display, web_page )


        # open index.html webfile and add
        # new URLS to the page
        url_code = '<a href="' + web_page + '">'+ country[0] + '</a> <b>Total Files :</b> ' + str(total_files_in_corpus) + \
                   '  <b>Total Pages :</b> '+ str(total_pages) + '<br> '
        file = open('index.html', 'a')
        file.write(url_code)
        file.write("\n")
        file.close()

        print('-------------')

    build_html_end()