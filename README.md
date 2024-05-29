# Medical-Chatbot-using-llama2
--bash
conda create -n mchatbot python==3.8 -y

--bash
conda activate mchatbot 

--bash
pip install -r requirements.txt

### create a '.env' file in root directory and add your Pinecone credentials as follows:

'''ini
PINECODE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
### download the model from 
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
'''
