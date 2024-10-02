from flask import Flask, jsonify, request, current_app as app
from flask_cors import CORS
import sys
import os
import time
# Import your modules after setting the path
sys.path.append("C:/Users/hajer/Downloads/response_to_call_for_proposal-main/response_to_call_for_proposal-main") 
from src.modules.information_extraction import get_response, intialize_gemini, get_file, extract_all_information, connect_to_mongo
from src.modules.response_generation import generate_all_response
from pymongo import MongoClient
import google.generativeai as genai

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': 'Access-Control-Allow-Origin'}})

    with app.app_context():
        # Initialize your model within the app context
        os.environ['GOOGLE_API_KEY'] = 'AIzaSyBJ7BpBwMDh78pQdWWnsmdBiRMwVzEKPe0'
        model = intialize_gemini(os.environ['GOOGLE_API_KEY'])
        model_2 = intialize_gemini("AIzaSyAYki-K0KB5vFV6exbMEpIsxdvKfxzY5r0")
        app.config["MODEL_2"] = model_2
        app.config['MODEL'] = model  
        import routes

    return app

app = create_app()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/get_information') 
def get_infos(file_path): 
    model = app.config['MODEL']  # Access the model here

    full_file = get_file(file_path)
    all_infos_cnfpt = extract_all_information(full_file)
    return all_infos_cnfpt

    form_data = request.form.to_dict()  # Get form data from the request
    ccap_path = form_data.get('ccap_path')  # Make sure to retrieve these from form data or context
    cctp_path = form_data.get('cctp_path')
    aapc_path = form_data.get('aapc_path')
    rc_path = form_data.get('rc_path')
@app.route('/generate_response', methods=['POST'])
def get_response_route(ccap_path,cctp_path,aapc_path,rc_path,form_data):
    

    model = app.config['MODEL']
    model_2 = app.config["MODEL_2"]
    mongo_uri = "mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority"
    
    try:
        client = connect_to_mongo(mongo_uri)
    except Exception as e:
        print("MongoDB connection error:", str(e))
        return jsonify({'error': 'Failed to connect to MongoDB'}), 500

    try:
        # Read and process each file
        ccap = get_file(ccap_path)
        cctp = get_file(cctp_path)
        aapc = get_file(aapc_path)
        rc = get_file(rc_path)
    except Exception as e:
        print("Error reading files:", str(e))
        return jsonify({'error': 'Error reading uploaded files'}), 500

    # Extract information from files
    all_infos = extract_all_information(ccap)
    print("Extracted information:", all_infos)

    # Generate response
    try:
        generate_all_response_result = generate_all_response(
            form_data['proj_name'], cctp, ccap, aapc, rc, form_data['name_organisation'], 
            form_data['pays'], form_data['numPubJOUE'], form_data['numAvisJAL_BOAMP'], 
            form_data['URL_JO'], form_data['num_et_rue'], form_data['code_postal'], 
            form_data['ville'], form_data['email'], form_data['num_tlp'], 
            form_data['perso_contact'], form_data['type_identifiant']
        )
        return jsonify(generate_all_response_result)
    except Exception as e:
        print("Error generating response:", str(e))
        return jsonify({'error': 'Error generating response'}), 500

    
    
@app.route('/upload', methods=['POST'])
def upload_file():
    required_fields = ['proj_name', 'numPubJOUE', 'pays', 'numAvisJAL_BOAMP', 'URL_JO', 
                        'num_et_rue', 'code_postal', 'ville', 'email', 'num_tlp', 
                        'perso_contact', 'type_identifiant']
    
    form_data = {}
    for field in required_fields:
        if field not in request.form:
            return jsonify({'error': f'{field} is missing'}), 400
        form_data[field] = request.form.get(field)

    file_paths = {}
    file_keys = ['ccapFile', 'cctpFile', 'aapcFile', 'rcFile']
    for file_key in file_keys:
        if file_key in request.files:
            file = request.files.get(file_key)
            if file.filename == '':
                return jsonify({'error': f'No selected file for {file_key}'}), 400

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            time.sleep(40)

            file_paths[file_key] = file_path
        else:
            return jsonify({'error': f'Missing {file_key}'}), 400

    try:
        print("Form data received:", form_data)  # Debug line
        print("File paths:", file_paths)  # Debug line
        response = get_response_route(file_paths['ccapFile'], file_paths['cctpFile'], 
                                      file_paths['aapcFile'], file_paths['rcFile'],form_data)
    except Exception as e:
        return jsonify({'error': print(e)}), 500

    return jsonify(response), 200
if __name__ == '__main__':
    app.run(debug=True)
