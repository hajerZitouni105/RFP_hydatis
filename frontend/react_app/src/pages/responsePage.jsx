import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import ReactLoading from 'react-loading';
import 'bootstrap/dist/css/bootstrap.min.css';

const transformText = (text) => {
  let transformedText = text.replace(/## (.*?):/g, '<h3>$1</h3>');
  transformedText = transformedText.replace(/\*\*(.*?)\*\*/g, '<h4>$1</h4>');
  transformedText = transformedText.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
  transformedText = transformedText.replace(/\n/g, '<br>'); // Replace newlines with <br> tags

  return transformedText;
};

const DictionaryTransformer = ({ dictionary }) => {
  const transformedDictionary = Object.entries(dictionary).reduce((acc, [key, value]) => {
    acc[key] = transformText(value);
    return acc;
  }, {});

  return (
    <div className="container">
      <div className="row">
        {Object.entries(transformedDictionary).map(([key, value]) => (
          <div key={key} className="col-md-6 mb-4">
            <div className="card shadow-sm formbold-form-group">
              <div className="card-body">
                <h2 className="card-title formbold-form-label">{key}</h2>
                <div className="card-text" dangerouslySetInnerHTML={{ __html: value }} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};


const ResponsePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { to_send } = location.state || {};
  const {proj_name, publicationNumber, country, notificationNumber,url, streetAddress,postalCode,city,email, phoneNumber,
     contactPerson, idType,files} = to_send || {}; // Ensure files are passed properly

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);

  useEffect(() => {
      if (!files) {
          navigate('/'); 
          return;
      }
// Accessing the files in the array

      const uploadFiles = async () => {
          const formData = new FormData();
          formData.append('ccapFile', files[0]);
          formData.append('cctpFile', files[1]);
          formData.append('aapcFile', files[2]);
          formData.append('rcFile', files[3]);
  
          // Add other form data
          formData.append('proj_name', proj_name);
          formData.append('numPubJOUE', publicationNumber);
          formData.append('pays', country);
          formData.append('numAvisJAL_BOAMP', notificationNumber);
          formData.append('URL_JO', url);

          formData.append('num_et_rue', streetAddress);
          formData.append('code_postal', postalCode);
          formData.append('ville', city);
          formData.append('email', email);
          formData.append('num_tlp', phoneNumber);
          formData.append('perso_contact', contactPerson);
          formData.append('type_identifiant', idType);
  

          try {
              const result = await axios.post('http://127.0.0.1:5000/upload', formData, {
                  headers: {
                      'Content-Type': 'multipart/form-data',
                  },
              });
              
              setResponse(result.data.filename); 
          } catch (err) {
              setError(err.message); 
          } finally {
              setLoading(false); 
          }
      };

      uploadFiles();
  }, [files[0],files[1],files[2],files[3], navigate,proj_name, publicationNumber, country, notificationNumber,url, streetAddress,postalCode,city,email, phoneNumber,
    contactPerson, idType]);

    if (loading) {
      return (
        <div className="d-flex flex-column justify-content-center align-items-center vh-100">
          <ReactLoading type="spin" color="#000" height={50} width={50} />
          <h2 className="mt-3">Loading...</h2>
          <p>Please wait while we process your file.</p>
        </div>
      );
    }
  
    if (error) {
      return (
        <div className="container mt-5">
          <div className="card shadow-sm">
            <div className="card-body text-center">
              <h2 className="card-title text-danger">Upload Failed</h2>
              <p className="card-text">{error}</p>
              <button className="btn btn-primary" onClick={() => navigate('/')}>Back to Form</button>
            </div>
          </div>
        </div>
      );
    }
  
    return (
      <div className="container mt-5">
        <h1 className="mb-4">Form Page</h1>
        <DictionaryTransformer dictionary={response} />
      </div>
    );
  };
  
  export default ResponsePage;


