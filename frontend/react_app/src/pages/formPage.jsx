import React, { useState } from 'react';
import './formPage_styles.css'; 
import { TagsInput } from "react-tag-input-component";
import { useNavigate } from 'react-router-dom';

const FormPage = () => {
    const [selected, setSelected] = useState([]);
    const [fileNames, setFileNames] = useState(["", "", "", ""]); // Array for 4 file names
    const [files, setFiles] = useState([null, null, null, null]); 

    const navigate = useNavigate();
    const [proj_name, setProjName] = useState("");
    const [publicationNumber, setPublicationNumber] = useState("");
    const [country, setCountry] = useState("");
    const [notificationNumber, setNotificationNumber] = useState("");
    const [url, setUrl] = useState("");
    const [streetAddress, setStreetAddress] = useState("");
    const [postalCode, setPostalCode] = useState("");
    const [city, setCity] = useState("");
    const [email, setEmail] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [contactPerson, setContactPerson] = useState("");
    const [idType, setIdType] = useState("");

    // Handle file change for multiple inputs
    const handleFileChange = (event, index) => {
        const file = event.target.files[0];
        if (file) {
            const newFiles = [...files];
            const newFileNames = [...fileNames];

            newFiles[index] = file; // Update the specific file by index
            newFileNames[index] = file.name; // Update the specific file name by index

            setFiles(newFiles); // Update the files array
            setFileNames(newFileNames); // Update the file names array
        }
    };

    const handleSubmit = () => {
        const to_send = {
            "proj_name": proj_name,
            "publicationNumber": publicationNumber,
            "country": country,
            "notificationNumber": notificationNumber,
            "url":url,
            "streetAddress": streetAddress,
            "postalCode": postalCode,
            "city": city,
            "email": email,
            "phoneNumber": phoneNumber,
            "contactPerson": contactPerson,
            "idType": idType,
            "selectedModules": selected,
            files: files.filter(file => file !== null)

        };

        // Navigate to the response page with the form data
        navigate('/response', { 
            state: { 
                to_send
            } 
        });
    };

    return (
        <div className="formbold-main-wrapper">
            <div className="formbold-form-wrapper">
                <form onSubmit={handleSubmit}>
                    {/* Input fields for form data */}
                    <div className="formbold-mb-5">
                        <label htmlFor="proj_name" className="formbold-form-label">Nom du projet:</label>
                        <input
                            type="text"
                            name="proj_name"
                            id="proj_name"
                            placeholder="Entrez le nom du projet"
                            className="formbold-form-input"
                            value={proj_name}
                            onChange={(e) => setProjName(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="publicationNumber" className="formbold-form-label">Numéro de publication au JOUE:</label>
                        <input
                            type="text"
                            name="publicationNumber"
                            id="publicationNumber"
                            placeholder="Entrez le numéro de publication au JOUE"
                            className="formbold-form-input"
                            value={publicationNumber}
                            onChange={(e) => setPublicationNumber(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="country" className="formbold-form-label">Pays:</label>
                        <input
                            type="text"
                            name="country"
                            id="country"
                            placeholder="Entrez le pays"
                            className="formbold-form-input"
                            value={country}
                            onChange={(e) => setCountry(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="notificationNumber" className="formbold-form-label">Numéro avis reçu du JAL ou du BOAMP:</label>
                        <input
                            type="text"
                            name="notificationNumber"
                            id="notificationNumber"
                            placeholder="Entrez le numéro d'avis reçu"
                            className="formbold-form-input"
                            value={notificationNumber}
                            onChange={(e) => setNotificationNumber(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="streetAddress" className="formbold-form-label">Numéro et rue:</label>
                        <input
                            type="text"
                            name="streetAddress"
                            id="streetAddress"
                            placeholder="Entrez le numéro et la rue"
                            className="formbold-form-input"
                            value={streetAddress}
                            onChange={(e) => setStreetAddress(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="url" className="formbold-form-label">URL Journal Officiel:</label>
                        <input
                            type="text"
                            name="url"
                            id="url"
                            placeholder="Entrez url "
                            className="formbold-form-input"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="postalCode" className="formbold-form-label">Code postal:</label>
                        <input
                            type="text"
                            name="postalCode"
                            id="postalCode"
                            placeholder="Entrez le code postal"
                            className="formbold-form-input"
                            value={postalCode}
                            onChange={(e) => setPostalCode(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="city" className="formbold-form-label">Ville:</label>
                        <input
                            type="text"
                            name="city"
                            id="city"
                            placeholder="Entrez la ville"
                            className="formbold-form-input"
                            value={city}
                            onChange={(e) => setCity(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="email" className="formbold-form-label">Email:</label>
                        <input
                            type="email"
                            name="email"
                            id="email"
                            placeholder="Entrez l'adresse e-mail"
                            className="formbold-form-input"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="phoneNumber" className="formbold-form-label">Numéro de téléphone:</label>
                        <input
                            type="text"
                            name="phoneNumber"
                            id="phoneNumber"
                            placeholder="Entrez le numéro de téléphone"
                            className="formbold-form-input"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="contactPerson" className="formbold-form-label">Personne ou personnes de contact:</label>
                        <input
                            type="text"
                            name="contactPerson"
                            id="contactPerson"
                            placeholder="Entrez la ou les personnes de contact"
                            className="formbold-form-input"
                            value={contactPerson}
                            onChange={(e) => setContactPerson(e.target.value)}
                        />
                    </div>
                    <div className="formbold-mb-5">
                        <label htmlFor="idType" className="formbold-form-label">Type de l'identifiant (N° de SIRET ou équivalent):</label>
                        <input
                            type="text"
                            name="idType"
                            id="idType"
                            placeholder="Entrez le type d'identifiant"
                            className="formbold-form-input"
                            value={idType}
                            onChange={(e) => setIdType(e.target.value)}
                        />
                    </div>
                
                    

                    {/* File upload inputs */}
                    <div className="mb-6 pt-4">
                        <label className="formbold-form-label formbold-form-label-2">Pièces jointes:</label>

                        <div className="formbold-mb-5 formbold-file-input" onClick={() => document.getElementById('fileInput').click()}>
                            <input
                                type="file"
                                id="fileInput"
                                onChange={(event) => handleFileChange(event, 0)}
                            />
                            <label htmlFor="fileInput">
                                <div>
                                    {fileNames[0] ? (
                                        <span className="formbold-file-name">{fileNames[0]}</span>
                                    ) : (
                                        <>
                                            <span className="formbold-drop-file">Déposez les fichiers ici</span>
                                            <span className="formbold-or"> Ou </span>
                                            <span className="formbold-browse">Parcourir</span>
                                        </>
                                    )}
                                </div>
                            </label>
                        </div>

                        <div className="formbold-mb-5 formbold-file-input" onClick={() => document.getElementById('fileInput1').click()}>
                            <input
                                type="file"
                            
                                id="fileInput1"
                                onChange={(event) => handleFileChange(event, 1)}
                            />
                            <label htmlFor="fileInput1">
                                <div>
                                    {fileNames[1] ? (
                                        <span className="formbold-file-name">{fileNames[1]}</span>
                                    ) : (
                                        <>
                                            <span className="formbold-drop-file">Déposez les fichiers ici</span>
                                            <span className="formbold-or"> Ou </span>
                                            <span className="formbold-browse">Parcourir</span>
                                        </>
                                    )}
                                </div>
                            </label>
                        </div>

                        <div className="formbold-mb-5 formbold-file-input" onClick={() => document.getElementById('fileInput2').click()}>
                            <input
                                type="file"
                                
                                id="fileInput2"
                                onChange={(event) => handleFileChange(event, 2)}
                            />
                            <label htmlFor="fileInput2">
                                <div>
                                    {fileNames[2] ? (
                                        <span className="formbold-file-name">{fileNames[2]}</span>
                                    ) : (
                                        <>
                                            <span className="formbold-drop-file">Déposez les fichiers ici</span>
                                            <span className="formbold-or"> Ou </span>
                                            <span className="formbold-browse">Parcourir</span>
                                        </>
                                    )}
                                </div>
                            </label>
                        </div>

                        <div className="formbold-mb-5 formbold-file-input" onClick={() => document.getElementById('fileInput3').click()}>
                            <input
                                type="file"
                                
                                id="fileInput3"
                                onChange={(event) => handleFileChange(event, 3)}
                            />
                            <label htmlFor="fileInput3">
                                <div>
                                    {fileNames[3] ? (
                                        <span className="formbold-file-name">{fileNames[3]}</span>
                                    ) : (
                                        <>
                                            <span className="formbold-drop-file">Déposez les fichiers ici</span>
                                            <span className="formbold-or"> Ou </span>
                                            <span className="formbold-browse">Parcourir</span>
                                        </>
                                    )}
                                </div>
                            </label>
                        </div>
                    </div>

                    {/* Submit button */}
                    <div>
                        <button type="submit" className="formbold-btn w-full">Soumettre</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default FormPage;
