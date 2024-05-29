from src.helper import load_pdf, text_split, download_hugging_face_embedding
from langchain.vectorstores import Pinecone
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import re

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
index_name = os.environ.get('index_name')

# print(PINECONE_API_KEY)
# print(index_name)

extracted_data=load_pdf("data//pocket-medicine_-the-massachusetts-general-hospital-handbook-of-internal-medicine.pdf")
text_chunks = text_split(extracted_data)
important_info = [doc.page_content.split('\nmetadata=')[0] for doc in text_chunks] # Removes unnecessary data
clean_info = [re.sub(r'[^\x00-\x7F]+', '', text) for text in important_info] # Cleans data by removing non ASCII values 
embeddings = download_hugging_face_embedding() # doenloading hugging face embedding
embedded_data = [[str(i), embeddings.embed_query(str(i))] for i in clean_info] # Convert cleaned text_chunks to embedded_data

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)

index.upsert(
    vectors = [
    {
         "id":str(i),
        "values": j,
    }
    for i,j in embedded_data[40:1040]  # You can only send 1000 embeddings to pinecone database in free account
],
    namespace= index_name)