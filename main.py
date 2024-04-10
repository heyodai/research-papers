#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import argparse
import requests
import re
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from classes import ArxivPaper, EmPaper

load_dotenv()
GOOGLE_DRIVE_PATH = os.getenv("GOOGLE_DRIVE_PATH")


# In[2]:


# Get CLI argument of URL
parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of the Emergent Mind paper")
parser.add_argument("--notes", help="Notes for the paper")
args = parser.parse_args()

# # Demo for Jupyter development
# args = argparse.Namespace()
# # args.url = 'https://www.emergentmind.com/papers/2404.01810'
# args.url = 'https://arxiv.org/abs/2304.15004'
# args.notes = 'This is a test note'
# args


# In[3]:


# Load necessary data
df = pd.read_excel(f"{GOOGLE_DRIVE_PATH}/arxiv_papers.xlsx")
article_id = args.url.split("/")[-1]
response = requests.get(args.url)
soup = BeautifulSoup(response.content, "html.parser")


# In[5]:


# Create the paper object
is_arxiv = bool(re.search("arxiv", args.url))
paper = (
    ArxivPaper(article_id, soup, args.notes)
    if is_arxiv
    else EmPaper(article_id, soup, args.notes)
)


# In[8]:


# Write data to dataframe
new_row = pd.DataFrame(
    {
        "arxiv_id": [article_id],
        "title": [paper.title],
        "publication_date": [paper.date],
        "abstract": [paper.abstract],
        "notes": [args.notes],
        "arxiv_url": [paper.arxiv_url],
        "em_url": [paper.em_url],
    }
)
df = pd.concat([df, new_row], ignore_index=True)

# Save the dataframe
df.to_excel(f"{GOOGLE_DRIVE_PATH}/arxiv_papers.xlsx", index=False)

