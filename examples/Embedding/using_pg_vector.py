
"""This example shows how to use PG Vector (Postgres) as a vector embedding database with llmware"""

""" (A) Python Dependencies - 

    As a first step, you should pip install two key dependencies not included in the llmware package:
    1.  pip3 install psycopg
    2.  pip3 install pgvector
    
    (B) Installing Postgres - 
    
    If you need help installing Postgres (with PG Vector), there are many great online sources and communities, e.g.,:
        -- PostgresSQL - https://www.postgresql.org/download/   (All OS)
        -- Mac OS Homebrew - https://wiki.postgresql.org/wiki/Homebrew - (brew install postgresql)
        -- Linux - https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql-linux/
        -- Windows - https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/
        -- Docker - https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/
        
    (C) Configurations - 
    
        -- set os.environ variables to 'automatically' pass in installing embedding
        -- os.environ["USER_MANAGED_PG_HOST"] = "localhost"
        -- os.environ["USER_MANAGED_PG_PORT"] = 5432
        -- os.environ["USER_MANAGED_PG_DB_NAME"] = "<DB that exists on Database>"
        -- os.environ["USER_MANAGED_PG_USER_NAME"] = optional 
        -- os.environ["USER_MANAGED_PG_PW"] = optional
        
"""


import os

from llmware.setup import Setup
from llmware.library import Library
from llmware.retrieval import Query


def build_lib (library_name, folder="Agreements"):

    # Step 1 - Create library which is the main 'organizing construct' in llmware
    print ("\nupdate: Step 1 - Creating library: {}".format(library_name))

    library = Library().create_new_library(library_name)

    # Step 2 - Pull down the sample files from S3 through the .load_sample_files() command
    #   --note: if you need to refresh the sample files, set 'over_write=True'
    print ("update: Step 2 - Downloading Sample Files")

    sample_files_path = Setup().load_sample_files(over_write=False)

    # Step 3 - point ".add_files" method to the folder of documents that was just created
    #   this method parses the documents, text chunks, and captures in MongoDB
    print("update: Step 3 - Parsing and Text Indexing Files")

    #   options:   Agreements | UN-Resolutions-500
    library.add_files(input_folder_path=os.path.join(sample_files_path, folder))

    return library


# start script

print("update: Step 1- starting here- building library- parsing PDFs into text chunks")

lib = build_lib("pgv_lib_0")

# optional - check the status of the library card and embedding
lib_card = lib.get_library_card()
print("update: -- before embedding process - check library card - ", lib_card)

print("update: Step 2 - starting to install embeddings")

#   alt embedding models - "mini-lm-sbert" | industry-bert-contracts |  text-embedding-ada-002
#   note: if you want to use text-embedding-ada-002, you will need an OpenAI key and enter into os.environ variable
#   e.g., os.environ["USER_MANAGED_OPENAI_API_KEY"] = "<insert your key>"

#   batch sizes from 100-500 usually give good performance and work on most environments
lib.install_new_embedding(embedding_model_name="industry-bert-contracts",vector_db="pg_vector",batch_size=300)

#   optional - check the status of the library card and embedding
lib_card = lib.get_library_card()
print("update: -- after embedding process - check updated library card - ", lib_card)

#   run a query
#   note: embedding_model_name is optional, but useful if you create multiple embeddings on the same library
#   --see other example scripts for multiple embeddings

#   create query object
query_pgv = Query(lib, embedding_model_name="industry-bert-contracts")

#   run multiple queries using query_pgv
my_search_results = query_pgv.semantic_query("What is the sale bonus?", result_count = 24)

for i, qr in enumerate(my_search_results):
    print("update: semantic query results: ", i, qr)

# if you want to delete the embedding  - uncomment the line below
# lib.delete_installed_embedding("industry-bert-contracts", "pg_vector")

#   optional - check the embeddings on the library
emb_record = lib.get_embedding_status()
for j, entries in enumerate(emb_record):
    print("update: embeddings on library: ", j, entries)

