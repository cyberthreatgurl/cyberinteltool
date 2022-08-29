#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:21:08 2022

@author: kdawg
"""
import PyPDF2
import translate as T

from langdetect import detect, DetectorFactory
from translate import Translator

from nltk_utils import preprocess


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
            for pn in range(0, pdf_obj.numPages):
                page = pdf_obj.getPage(pn)

                text = page.extractText().lower()
                # translation = translator.translate(text)
                langText = detect(text)
                if langText == 'zh-cn':
                   translator = Translator(to_lang='en', from_lang='zh')
                   text = translator.translate(text)
                cleaned_list = preprocess(text)
                corpus_list.append(cleaned_list)

                text_list.append((pdf, pn))
            #               print(pdf_obj.extractText())

                
            print('File '+ pdf + ' is ' + langText)
        except Exception as exc:
            exc

    pdf_file_obj.close()
    return corpus_list, text_list
