#!/usr/bin/env python
# coding: utf-8

# Execute the `main.py` script in batches from URLs in the `batch.txt` file.

# In[ ]:


import os


# In[ ]:


# Activate venv
os.system('source .venv/bin/activate')


# In[ ]:


# Open batch.txt
with open('batch.txt', 'r') as f:
    # Read the file
    lines = f.readlines()

    for url in lines:
        # Remove the trailing newline character
        url = url.strip()
        
        # Execute the command
        os.system(f'python main.py {url}')

