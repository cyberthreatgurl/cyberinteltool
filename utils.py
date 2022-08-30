#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:23:52 2022

@author: kdawg
"""



#
# Checks to see if a multidimensional
# list is empty
def isListEmpty(inList):
    if isinstance(inList, list):  # Is a list
        return all(map(isListEmpty, inList))
    return False  # Not a list



# sort the tfidf output
def Sort(tfidf_tuples):
    "This sorts based on the second value in our tuple, the tf-idf score"
    tfidf_tuples.sort(key=lambda x: x[1], reverse=True)
    return tfidf_tuples