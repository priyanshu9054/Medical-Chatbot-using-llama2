from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embedding
from pinecone import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
from src.prmopt import prompt_tempelate
import os
import time
import sys

app=Flask(__name__)


load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
index_name = os.environ.get('index_name')
pc = Pinecone(api_key=PINECONE_API_KEY)


embeddings = download_hugging_face_embedding()

PROMPT = PromptTemplate(template=prompt_tempelate, input_variables=["context",'question'])
chain_type_kwargs={"prompt":PROMPT}

# Load the Llama2 model
llm = CTransformers(
    model='model\\llama-2-7b-chat.ggmlv3.q2_K.bin',
    model_type='llama',
    config={'max_new_tokens': 256, 'temperature': 0.01}
)


def get_llama_response(context,question):
    
    PROMPT = PromptTemplate(template=prompt_tempelate, input_variables=["context",'question'])
    # Generate response from llama model
    response = llm.invoke(PROMPT.format(context=context,question=question))

    return response

# response=get_llama_response(retriever.matches[0]['id'],Question)
# print(response)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print("Processing your request...")
    sys.stdout.flush()  # Flush the buffer to ensure immediate printing

    # Measure the start time
    start_time = time.time()
    print(input)
    query_result = embeddings.embed_query(input)
    print("embeddings done")
    retriever = pc.Index(index_name).query(
        namespace=index_name,
        vector=query_result,
        top_k=2,
        include_values=True,
    )
    print(retriever)
    result = get_llama_response(retriever.matches[0]['id'], input)

    # Measure the end time
    end_time = time.time()
    duration = end_time - start_time

    print("Request processed in {:.2f} seconds.".format(duration))
    return str(result)

        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000 ,debug=True)