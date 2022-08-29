############################################################
# Date:      July 29. 2022
# Coder:     Kelly Shaw
# EMail:     cyberintelgurl@gmail.com
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
#   with files of interest.  Look for details in corpus-struct.txt

# - This program then generates an index.html file and a web page for
#   each country that shows the LDA visualization of the cyber-defense
#   and cyber-offense technologies being researched and developed.
# - You can manually tweak the "stop words" until you are happy
#   that all the extraneous words have been removed from the
#   corpus.
#
# Version
# 1.1 - Cleaned-up                                          July 29, 2022   AKS
# 1.1a - Added TF-IDF Model and started JSON file input     Aug 2, 2022     AKS
#
import nltk
import gensim
import warnings
import json
import os
import pickle
import glob
import translate
import pandas as pd
import PyPDF2
import pyLDAvis
import langdetect

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

from database import create_database, pdf_database_write
from create_webpage import *
from pdf_utils import pdf_extractor
from nltk_utils import *

from utils import isEmptyList, Sort



from pyLDAvis import gensim_models as gensimvis
from pandas import json_normalize

# get rid of those pesky deprecation warnings.
warnings.filterwarnings("ignore", category=DeprecationWarning)

# nltk.download('stopwords')

#
if __name__ == "__main__":

    # create the database
    #create_datebase()
    
    #
    # build a list of the countries for patents and academic
    # for all academic papers written in English, regardless of
    # country

    # read in USPTO Patent json files
#    json_extractor()

    sources = ["patents", "academic"]

    # this section needs to be manually updated
    # as new country data is found.  Of course,
    # this needs to be done automatically in the future.
    countries = [
        ("australia", "oceania"),
        ("austria", "europe"),
        ("belarus", "europe"),
        ("belgium", "europe"),
        ("canada", "northamerica"),
        ("china", "asia"),
        ("cyprus", "europe"),
        ("czechrepublic", "europe"),
        ("denmark", "europe"),
        ("ecuador", "southamerica"),
        ("finland", "europe"),
        ("france", "europe"),
        ("ghana", "africa"),
        ("germany", "europe"),
        ("greece", "europe"),
        ("india", "asia"),
        ("iraq", "asia"),
        ("israel", "mideast"),
        ("italy", "europe"),
        ("japan", "asia"),
        ("jordan", "asia"),
        ("liechtenstein", "europe"),
        ("morocco", "africa"),
        ("netherlands", "europe"),
        ("norway", "europe"),
        ("nigeria", "africa"),
        ("pakistan", "asia"),
        ("poland", "europe"),
        ("portugal", "europe"),
        ("romania", "europe"),
        ("russia", "asia"),
        ("saudiarabia", "mideast"),
        ("serbia", "europe"),
        ("singapore", "asia"),
        ("southafrica", "africa"),
        ("southkorea", "asia"),
        ("spain", "europe"),
        ("srilanka", "asia"),
        ("sweden", "europe"),
        ("slovakrepublick", "europe"),
        ("slovenia", "europe"),
        ("switzerland", "europe"),
        ("turkey", "europe"),
        ("taiwan", "asia"),
        ("uk", "europe"),
        ("ukraine", "europe"),
        ("us", "northamerica"),
    ]

    build_html_head()
    build_html_body_frame()
    # The source patent and academic files are in the 'corpus' folder.
    # and are further grouped by region (mideast, asia, etc.) and
    # country
    # the corpus folder should be in the same folder as the main.py file
    data_folder = "corpus"
    cur_dir = os.getcwd()
    abs_path = cur_dir + "/" + data_folder

    # iterate through all a countries (patent and academic papers
    # before foing analysis on the text, so that each country
    # has a unique file.  Future updates will allow this to be
    # more flexible
    for country in countries:

        # build the path to this folder
        # grab all of the files from this particular folder
        pdf_path = "**/" + country[0] + "/*.pdf"

        pdfs = glob.glob(pdf_path, recursive=True)
        if len(pdfs) != 0:
            print("Country : " + country[0])
            print("Number of " + country[0] + " " + " files : " + str(len(pdfs)))
        else:
            print("Their are no data files for " + country[0])
            print("-------------")
            continue
        corpus_list = []
        text_list = []

        # read every page of the pdf file into the
        # corpus list.
        for pdf in pdfs:
            # call the extraction function
            corpus_list, text_list = pdf_extractor(pdf, corpus_list, text_list)
            #write corpus to database
            pdf_database_write(pdf, text_list)
            
        # Create a dictionary representation of the documents.
        dictionary = Dictionary(corpus_list)

        # While files were found in this folder, nothing was parsed
        # from them.  This is probably due to language issues that
        # have yet to be coded for.
        if dictionary == 0:
            print("Corrupt {0}  files.".format(country[0]))
            continue

        # Filter out words that occur less than 5 times
        # in the whole corpus or more than 60% of the documents.
        dictionary.filter_extremes(no_below=5, no_above=0.50)

        corpus = [dictionary.doc2bow(pdf_file) for pdf_file in corpus_list]

        if len(corpus) == 0 or isListEmpty(corpus):
            print("No usable files for this country, corpus empty.")
            continue
        else:
            total_files_in_corpus = len(pdfs)

        pickle.dump(corpus, open("corpus.pkl", "wb"))
        #    # Make a index to word dictionary.
        dictionary.save("dictionary.gensim")

        temp = dictionary[0]  # This is only to "load" the dictionary into memory..

        id2word = dictionary.id2token
        total_pages = len(corpus)

        print("Total number of pages parsed in this corpus: %d" % total_pages)
        print("-------------")
        print("")

        #
        # create a TF-IDF model
        freq_model = gensim.models.TfidfModel(corpus)

        # Create TF-IDF scores for the ``bow_corpus`` using our model
        corpus_tfidf = freq_model[corpus]

        td = {}
        for document in corpus_tfidf:
            for token_id, score in document:
                current_score = td.get(dictionary.get(token_id), 0)
                if current_score < score:
                    td.update([(dictionary.get(token_id), score)])

        # Sort the items of ``td`` into a new variable ``sorted_td``
        # the ``reverse`` starts from highest to lowest
        sorted_td = sorted(td.items(), key=lambda kv: kv[1], reverse=True)
        print("Term\t\t\t\tWeight")
        print("-------------------------")
        for term, weight in sorted_td[:5]:  # Print the top  terms in the entire corpus
            print("{0:s}\t\t\t\t{1:.2f}".format(term, weight))

        # Train the topic model
        model = LdaModel(
            corpus=corpus, id2word=id2word, iterations=100, num_topics=5, alpha="auto"
        )
        model.save("model1,gensim")

        topics = model.print_topics(num_words=5)
        for topic in topics:
            print(topic)

        lda_display = gensimvis.prepare(model, corpus, dictionary)
        web_page = country[1] + "-" + country[0] + "-LDA.html"
        pyLDAvis.save_html(lda_display, web_page)

        # open index.html webfile and add
        # new URLS to the page
        url_code = (
            '<a href="'
            + web_page
            + '">'
            + country[0]
            + "</a> <b>Total Files :</b> "
            + str(total_files_in_corpus)
            + "  <b>Total Pages :</b> "
            + str(total_pages)
            + "<br> "
        )
        file = open("index.html", "a")
        file.write(url_code)
        file.write("\n")
        file.close()

        print("-------------")

    build_html_end()
