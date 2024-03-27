#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import argparse
import requests
import re
import datetime
from bs4 import BeautifulSoup
from openpyxl import Workbook

GOOGLE_DRIVE_PATH = '/Users/odai/Library/CloudStorage/GoogleDrive-heyodai@gmail.com/My Drive'


# In[2]:


# # Initial dataframe setup
# df = pd.DataFrame(
#     columns=[
#         "arxiv_id",
#         "title",
#         "publication_date",
#         "abstract",
#         "notes",
#         "arxiv_url",
#         "em_url",
#     ]
# )

# df.to_excel(f"{GOOGLE_DRIVE_PATH}/arxiv_papers.xlsx", index=False)
# df.head()


# In[5]:


# Get CLI argument of URL
parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of the Emergent Mind paper")
parser.add_argument("--notes", help="Notes for the paper")
args = parser.parse_args()

# # Demo for Jupyter development
# args = argparse.Namespace()
# args.url = 'https://www.emergentmind.com/papers/2403.14562'
# args.notes = 'This is a test note'
# args


# In[6]:


# Load the excel file
df = pd.read_excel(f"{GOOGLE_DRIVE_PATH}/arxiv_papers.xlsx")
df.head()


# In[7]:


# Load the URL into a BeautifulSoup object
response = requests.get(args.url)
soup = BeautifulSoup(response.content, "html.parser")
soup


# In[8]:


# Get the title from soup

"""
<h1 class="text-[16px] md:text-[19px] leading-[1.4] md:leading-[1.3] text-[hsl(245,20%,50%)] no-underline font-sitka font-semibold inline">
          The Era of Semantic Decoding
        </h1>
"""

title = soup.find("h1").text.strip()
title


# In[10]:


# Get the Arxiv ID
# Iterate through spans until we regex match the arxiv ID structure

"""
<span class="text-[#5B5852] text-[13px] leading-5 font-sitka">(2403.14562)</span>
"""

arxiv_id = None
for span in soup.find_all("span"):
    match = re.match(r"\((\d{4}\.\d{5})\)", span.text)
    if match:
        arxiv_id = match.group(1)
        break
    
arxiv_id

# We can also construct the URLs from the arxiv ID
arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
em_url = f"https://www.emergentmind.com/papers/{arxiv_id}"


# In[11]:


# Find the publication date

"""
<div class="text-[#5B5852] text-[14px] md:text-[16px] font-sitka mt-2 leading-[1.4]">
        Published Mar 21, 2024
            in
            <span class="" x-tooltip.raw="Computation and Language">cs.CL</span>
                <span class="-ml-[3px]">,</span>
            <span class="" x-tooltip.raw="Artificial Intelligence">cs.AI</span>
                <span class="-ml-[3px]">,</span>
            <span class="" x-tooltip.raw="Human-Computer Interaction">cs.HC</span>
                <span class="-ml-[3px]">,</span>
            <span class="" x-tooltip.raw="Multiagent Systems">cs.MA</span>
                and

          by <a class="border-b border-gray-100 hover:text-stone-500" href="https://www.emergentmind.com/search?q=Maxime+Peyrard">Maxime Peyrard</a>, <a class="border-b border-gray-100 hover:text-stone-500" href="https://www.emergentmind.com/search?q=Martin+Josifoski">Martin Josifoski</a>, and <a class="border-b border-gray-100 hover:text-stone-500" href="https://www.emergentmind.com/search?q=Robert+West">Robert West</a>.
      </div>
"""

# For the date, we can look for the text "Published" and extract the date
date = None
for div in soup.find_all("div"):
    if "Published" in div.text:
        match = re.search(r"Published (\w+ \d{1,2}, \d{4})", div.text)
        if match:
            date = match.group(1)
        break
    
# This comes out like 'Mar 21, 2024', so we can parse it with datetime
date = datetime.datetime.strptime(date, "%b %d, %Y").date()
date = date.strftime("%Y-%m-%d")
date


# In[13]:


# To get the abstract, find the H3 tag with the text "Abstract"
# The next sibling is the actual abstract

abstract = None
for h3 in soup.find_all("h3"):
    if h3.text.strip() == "Abstract":
        abstract = h3.find_next_sibling("div").text.strip()
        break
    
abstract


# In[14]:


# Write data to dataframe
new_row = pd.DataFrame(
    {
        "arxiv_id": [arxiv_id],
        "title": [title],
        "publication_date": [date],
        "abstract": [abstract],
        "notes": [args.notes],
        "arxiv_url": [arxiv_url],
        "em_url": [em_url],
    }
)

df = pd.concat([df, new_row], ignore_index=True)

# Save the dataframe
df.to_excel(f"{GOOGLE_DRIVE_PATH}/arxiv_papers.xlsx", index=False)

