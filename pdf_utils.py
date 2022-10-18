#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:21:08 2022

@author: kdawg
"""
import PyPDF2
import logging
import tika

from database import pdf_database_write
from tika import parser
from langdetect import detect, DetectorFactory
from translate import Translator

from nltk_utils import preprocess

def tika_pdf_extractor(pdf, corpus_list, text_list):
    parsed_pdf = parser.from_file(pdf)

    text = parsed_pdf['content']
    metadata_dict = parsed_pdf['metadata']
    title = metadata_dict['title']
    author = metadata_dict['Author']  # capturing all the names from lets say 15 pages.
    # Just want it to capture from first page
    pages = metadata_dict['xmpTPg:NPages']
    text = text.lower()

    # translation = translator.translate(text)
    langText = detect(text)
    if langText == '!zh-cn':
        translator = Translator(to_lang='en', from_lang='zh')
        text = translator.translate(text)

    cleaned_list = preprocess(text)
    corpus_list.append(cleaned_list)

    text_list.append(pdf)

    pdf_database_write(pdf,title, text)

    logging.info('File ' + pdf + ' is ' + langText)

    return corpus_list, text_list

# function to extract text from PDF files
#
def pdf_extractor(pdf, corpus_list, text_list):
    """Extract the text of pdfs and return a dictionary with
   the file name as a key, and the value being a list of the pages
   and the containing texts
    """
    with open(pdf, "rb") as pdf_file_obj:
        try:
            # translator = Translator(to_lang="English")
            pdf_obj = PyPDF2.PdfReader(pdf_file_obj, strict=False)

            DetectorFactory.seed = 0

            # read each page of the pdf file and
            # grab the text from it
            file_text = ""
            for pn in range(0, pdf_obj.numPages):
                page = pdf_obj.getPage(pn)

                text = page.extractText().lower()
                # translation = translator.translate(text)
                langText = detect(text)
                if langText == '!zh-cn':
                   translator = Translator(to_lang='en', from_lang='zh')
                   text = translator.translate(text)
                file_text = file_text + " " + text
                cleaned_list = preprocess(text)
                corpus_list.append(cleaned_list)

                text_list.append((pdf, pn))
            #               print(pdf_obj.extractText())


            pdf_database_write(pdf, file_text)

            logging.info('File '+ pdf + ' is ' + langText)
        except Exception as exc:
            exc

    pdf_file_obj.close()
    return corpus_list, text_list
