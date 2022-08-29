#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:15:35 2022

@author: kdawg
"""

# Build the header section of the
# output index.html page
def build_html_head():
    html_heading_text = """
    <html>
        <head><title>Cyber Security Defense and Offense Topic Modeling</title>
        <h1>Topic Modeling of Cyber Offense/Defensive Terms</h1>
        </head>
    """
    file = open("index.html", "w")
    file.write(html_heading_text)
    file.close()


# build the body section of the
# output index.html page.
def build_html_body_frame():
    html_body_text = """
        <body bgcolor="white">
    """
    file = open("index.html", "a")
    file.write(html_body_text)
    file.close()


# Build the end section of the index.html
# output file.
def build_html_end():
    html_end_text = """
        </body>
    </html>"""
    file = open("index.html", "a")
    file.write(html_end_text)
    file.close()
