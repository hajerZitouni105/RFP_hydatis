import PyPDF2
from deep_translator import GoogleTranslator
from langdetect import detect
import re
import pathlib
import textwrap
import google.generativeai as genai
#from google.colab import userdata
#from IPython.display import display
#from IPython.display import Markdown
from vertexai.generative_models import GenerativeModel, Part
import os
from pymongo import MongoClient


def read_pdf(filename):

  with open(filename, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text

def detect_lang(resume_text) :
    try :
        lang = detect(resume_text)
        if lang == 'fr' :
            final_text=list()
            for i in range(0, len(resume_text), 4999):
                translation = GoogleTranslator(source='auto', target='en').translate(resume_text[i:i+4999], dest='en')
                final_text.append(translation)
            return ' '.join(final_text)
        else :
            return resume_text
    except Exception as e:
        return resume_text
def replace_points(text) :
    """
    this function replaces multiple points by a back to line special character
    """
    processed_text = re.sub(r'\.{2,}', '\n', text)
    return processed_text
def get_file(file_path) :
  text = read_pdf(file_path)
  processed_text = replace_points(text)
  translated_text = detect_lang(processed_text)
  return translated_text
def intialize_gemini(api_key) :
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
  return model
def to_markdown (text):
  text = text.replace('• ','**')
  return Markdown(textwrap.indent(text,'>',predicate=lambda _:True))
def get_response(model,prompt,top_k,top_p,temperature=0.5):
    generation_config= genai.types.GenerationConfig(
        temperature=temperature, top_k=top_k, top_p=top_p
    )
    response = model.generate_content(prompt, generation_config=generation_config)
    return response.parts[0].text
def extract_infos(file) :
  prompt_context_sources=f"""From the provided text, extract the administrative clauses and conditions for the contract.
   Identify key elements such as: market purpose, scope of the mission, constituent parts of the contract, legislation governing the contract,
   conditions of execution, contract amount and nature of prices, execution deadlines, guarantees and sureties, modifications and amendments,
   reception and verification of services, insurance obligations, terms of payment, delay penalties, contract termination conditions,
   and dispute resolution procedures and finnaly mention if there is any risk, confusion or missing information such as: ect, ....
   Extract word by word from the text, and make it clear and concise. Only use the provided document, do not come up with new requirements.
   Please provide from the document the sections from which you extracted your information even the last part of confusions and missing infos (Mention the exact source of risk,
   with the detail which you based on to identify it as a risk. Mention the source of the risk, which is the section of the document by its index and number).
   The output will be in this form : The information is : -- info . The source is : -- source.And please enumerate the informations.
   Here's the full document: \n {file}"""
  response = get_response(prompt_context_sources,50,0.7)
  return response

def extract_all_information(file):
  infos = extract_infos(file)

  return {
      "infos": infos
      }

def connect_to_mongo(mongo_uri):
  """Connects to a MongoDB database given the URI."""
  client = MongoClient(mongo_uri)
  return client

def update_or_add_db(column, mongouri, data):
    client = connect_to_mongo(mongouri)
    db = client['hydatis_cfp']
    collection = db['responses']
    existing_doc = collection.find_one({"name": data['name']})

    if existing_doc:
        collection.update_one({"name": data['name']}, {"$set": {column: data[column]}})
        print(f"Document for '{data['name']}' updated successfully.")
    else:
        new_doc = {"name": data['name'], column: data[column]}
        insert_result = collection.insert_one(new_doc)
        print(f"New document for '{data['name']}' inserted with ID: {insert_result.inserted_id}")

    client.close()

