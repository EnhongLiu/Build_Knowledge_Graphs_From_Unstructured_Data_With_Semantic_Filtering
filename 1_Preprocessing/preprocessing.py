import pandas as pd
import numpy as np
import re
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pprint
import uuid


# Read in data
jds_metadata = pd.read_csv('./jds_metadata.csv')
animal_metadata = pd.read_csv('./animal_metadata.csv')

# Cleaning to drop rows with missing abstracts
jds_cleaned = jds_metadata.copy().dropna(subset=['Abstract'])
animal_cleaned = animal_metadata.copy().dropna(subset=['Abstract'])

def extract_abstract(text):
    match = re.search(r"Author information:.*?\n\n(.*?)\n\n(?:Copyright|DOI|PMID)", text, re.DOTALL)
    if match:
        abstract = match.group(1).strip()
        abstract = re.sub(r'\s+', ' ', abstract)
        return abstract
    return None

jds_cleaned['Pure Abstract'] = jds_cleaned['Abstract'].apply(extract_abstract)
animal_cleaned['Pure Abstract'] = animal_cleaned['Abstract'].apply(extract_abstract)

# Combine JDS and Animal
journal_df = pd.concat([jds_cleaned,animal_cleaned])[['Title','Pure Abstract','Authors','Publication Date','DOI','Link','Affiliations','PubMed ID','Publication Year','Country']]

journal_df_cleaned = journal_df.dropna(subset=['Pure Abstract'], how='any')



# Convert the extracted text into Document objects
documents = [
    Document(
        page_content=row['Pure Abstract'], 
        metadata={col: row[col] for col in jds_test.columns if col != 'Pure Abstract'}
    )
    for _, row in jds_test.iterrows()
]

# Initialize the text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

# Split the documents into chunks
chunks = splitter.split_documents(documents)



def documents2Dataframe(documents):
    rows = []
    for chunk in documents:
        row = {
            "text": chunk.page_content,
            **chunk.metadata,
            "chunk_id": uuid.uuid4().hex,
        }
        rows = rows + [row]

    df = pd.DataFrame(rows)
    return df


df_chunks = documents2Dataframe(chunks)

print(df_chunks.shape)
# Output the DataFrame
display(df_chunks.head())  
