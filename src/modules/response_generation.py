import sys
#sys.path.append("C:/Users/rayen/Desktop/programming/hydatis_internship/final_project") 
import time
from src.modules.information_extraction import get_response,intialize_gemini,get_file,extract_all_information,connect_to_mongo
import os
def get_values(client,column_name) :
  db = client['hydatis_cfp']
  collection = db['responses']
  contexts = [doc for doc in collection.find()]
  rows = [doc.get(column_name, "") for doc in contexts]
  return rows
def generate_context(name,file) :
  previous_contexts= get_values(client,'context')
  prompt = f"""Given this project document, {file} I want you to create a project offer context.
Here are some examples of contexts from previous projects, that you will base on in order to generate the new context. Just base on the structure, not the information included :
{"context: ".join(previous_contexts)}
each reference context is starting with context:
Provide for each value proposition how can we achieve that value, example : Accompaigning during the phase of evolution maintenance, how ? by providing technical and methodological support to guarantee the reliability and sustainability of the tool based on Windev client-server software. This is just an example, apply the same way of thinking to any part you add.
I don't want general headlines, I need the how.
You can add the references from the previous documents.
My company's name is hydatis
You can add this paragraph, but adjusted based on the need at the end of the section : The HYDATIS GROUP is mobilizing, for this market, to demonstrate the relevance of our technical approach and the understanding of the objectives of the services associated with OUTSOURCING OF IT DEVELOPMENTS AND MANAGEMENT OF DEVELOPMENT PROJECTS.
Our teams are very eager to support you in the complex and strategic maintenance of this complete project, and they are available to provide you with any additional information you may need.

  """
  response = get_response(prompt,600,0.7,0.9)
  return response
def get_pub_infos(name_organisation,pays,num_pub_JOUE,num_avis_JAL_BOAMP,URL_JO):
  return f""" **Partie I : Informations concernant la procédure de passation et de marché et de l'acheteur**.\n
  **Informations concernant la publication**\n
   Pour les procédures de passation de marché dans le cadre desquelles un appel à concurrence a été publié au Journal officiel de l'Union Européenne,
   les informations requises au titre de la partie I seront automatiquement récupérées par voie électronique pour autant que le service DUME électronique soit utilisé pour générer et remplir le DUME.
   \n Référence de l'avis pertinent publié au Journal officiel de l'Union européenne:
   \nN° de publication au JOUE : {num_pub_JOUE} .
  \n N° avis reçu du JAL ou du BOAMP : {num_avis_JAL_BOAMP} .

   \n URL du JO : {URL_JO} .
   \n Si aucun appel d'offres n'est publié au Journal officiel, ou s'il n'est pas nécessaire d'en publier, l'autorité ou l'entité contractante doit identifier clairement la procédure de passation de marché
   (par exemple, la référence à une publication de niveau national)

   \n **Identité de l'acheteur** \n
   Nom de l'acheteur : {name_organisation} .\n
   Pays : {pays}
   """

def get_infos_passation(context,offer):
  previous_contexts= get_values(client,'dume1')

  prompt=f"""I am providing you with the context of a public contract: {context}, as well as the corresponding CCTP document: {offer}. Based on this informations, generate only the following sections of the first part of the European Single Procurement Document (ESPD):
Structure the generated text clearly and in accordance with the following format:
\n 1. **Contract Objective**: extract the objective of the contract from the context in approximately 2 lines.(mention modules if exists)

\n 2. **Brief Description**: extract the context of the contract (usually the first paragraph in the context provided) in 4 to 5 lines. (mention also modules, applications not sections)

\n 3. **Reference Number Assigned by the Buyer**: Extract the reference number directly from the CCTP document and indicate only the number.

note: please when there is an abreviation mention them and expand them.In 3. extract only the number don't add any other detail
Here are some examples of the sections of the Informations relating to the procurement procedure Subject of the contract of the European Single Procurement Document (ESPD) from previous projects, that you will base on in order to generate the new sections. Just base on the structure, not the information included :
{"context: ".join(previous_contexts)}
"""
  response = get_response(prompt,600,0.7)
  return response

def get_infos_operateur(num_et_rue,code_postal,ville,pays,email,num_tlp,perso_contact,type_identifiant,lots_passation_marhe="Pas d'information sur les lots"):
  return f"""***Partie II : Informations concernant l'opérateur économique**.\n\n
  **A. Informations concernant l'opérateur économique**\n

  \n Nom : HYDATIS.
  \n Numéro et rue : {num_et_rue}.
  \n Code postal : {code_postal}.
  \n Ville : {ville}.
  \n Pays : {pays}.
  \n Adresse internet : www.hydatis.com.
  \n Adresse électronique : {email}.
  \n Téléphone : {num_tlp}.
  \n Personne ou personnes de contact : {perso_contact}.
  \n Type d'identifiant (SIRET, TVA, autre) : {type_identifiant}.

  \n Etes-vous une micro, une petite ou une moyenne entreprise ? : Réponse : Oui.

  \n Uniquement dans le cas où le marché est réservé : Êtes-vous un atelier protégé, une "entreprise sociale" ou prévoyez-vous l'exécution du marché dans le cadre de programmes d'emplois protégés ? Réponse : [oui/non]

  \n Le cas échéant, êtes-vous inscrit sur une liste officielle d'opérateurs économiques agréés ou êtes-vous muni d'un certificat équivalent [par exemple dans le cadre d'un système national de (pré)qualification] ? Réponse : [oui/non]

  \n Etes-vous en mesure de fournir un certificat en ce qui concerne le paiement des cotisations de sécurité sociale et des impôts et taxes ou de fournir des informations permettant au pouvoir adjudicateur ou à l'entité adjudicatrice
  de l'obtenir directement en consultant une base de données nationale dans un État membre qui est accessible gratuitement ? [oui/non]

  \n Participez-vous à la procédure en groupement ? Réponse :[oui/non]

  \n S'il y a lieu, indiquez le ou les lots que vous souhaitez soumettre à la procédure de passation de marché : Réponse :{lots_passation_marhe}"""

def get_infos_represantants():
  return f"""***B. Informations relatives aux représentants de l'opérateur économique**\n
Nom : [nom1]\n
Prénom : [prenom1]\n
Date de naissance : [date_naissance1]\n
Lieu de naissance : [lieu_naissance1]\n
Numéro et rue : [num_rue1]\n
Code postal : [code_postal1]\n
Ville : [ville1]\n
Pays : [pays1]\n
Téléphone : [num_tlp1]\n
Courriel : [courriel1]\n
Fonction/agissant en qualité de : [fonction1]\n
Forme juridique de l'opérateur économique/informations générales : [forme_juridique1]\n\n\t
Nom : [nom2]\n
Prénom : [prenom2]\n
Date de naissance : [date_naissance2]\n
Lieu de naissance : [lieu_naissance2]\n
Numéro et rue : [num_rue2]\n
Code postal : [code_postal2]\n
Ville : [ville2]\n
Pays : [pays2]\n
Téléphone : [num_tlp2]\n
Courriel : [courriel2]\n
Fonction/agissant en qualité de : [fonction2]\n
Forme juridique de l'opérateur économique/informations générales : [forme_juridique2]


   """
def get_capacités_autres_entités_et_sous_traitants():
  return f"""**C. Informations relatives au recours aux capacités d'autres entités**\n\n
   Allez-vous vous appuyer sur la ou les capacités d’un autre opérateur économique pour justifier que vous rentrez dans les critères de sélection ? Réponse : [oui/non]
\n
  **D. Informations concernant les sous-traitants**\n\n
   Avez-vous l’intention de sous-traiter une partie du contrat à des tiers ? Réponse :[oui/non]"""

def generate_PROCEDURE_FORM_OF_PUBLIC_CONTRACT(ccap,aapc):
  previous_contexts= get_values(client,'pae1')

  prompt=f"""Analyze the provided CCAP document {sydev} and generate the section '1. PROCEDURE AND FORM OF THE PUBLIC CONTRACT' of the Project Act of Engagement (AE) by extracting the relevant information. The section should include the following elements:

Type of Contract and Duration:
type of contract:
duration:
Identify and mention the type of contract (Framework agreement, subsequent contract, etc.).
Specify the exact duration of the contract, starting from its notification.
Extract in paragraph form the minimum and maximum amounts of the contract, in euros excluding taxes, as well as the applicable CCP articles .
Contracting Authority:

Extract and mention the full name, address, and contact details (telephone number) of the contracting authority.
Contract Signatory:

Specify the name, first name, and title of the signatory of the public contract, including references to the deliberations or decrees that authorize these individuals to sign.
Person Authorized to Provide Information on Pledges or Assignment of Receivables:

Mention the name and position of the responsible person, along with their contact details.
Assigning Accountant and Budgetary Allocation:

Provide details about the assigning accountant, including the address and telephone number, as well as the information related to the budgetary allocation (account number and chapter).
Here are some examples of the first section of the Draft Contract of Engagement from previous projects, that you will base on in order to generate the new sections. Just base on the structure, not the information included :
{"pae1".join(previous_contexts)}. this is the Public Call for Tender document {sydev3} may include some informations about the contract signatory and the signatory of the public contract"""
  response = get_response(prompt,600,0.7)
  return response
def generate_sections_4_to_10(ccap,rc):
  previous_contexts= get_values(client,'pae1')

  prompt=f"""Analyse le document CCAP {sydev} et le document Règlement de Consultation {sydevRC} fournies et génère les sections '4.Durée de validité des offres', '5.Prix', '6.Délai d’exécution', '7. Sous-traitance', '8. Paiements', '9. Garantie', et '10. Échanges dématérialisés' du Projet Acte d'Engagement (AE). Les informations à extraire et structurer sont les suivantes :

4.Durée de validité des offres :

Décris la période de validité des offres compris:
- la durée (en jours)
- la date de début
- la date de fin ,si la date de fin n'existe pas écrire: 'jusqu’à l’attribution du marché public'.
les 2 dates doivent etre mentionner nécessairement.

5.Prix :

Fournis une explication sur la manière dont les prix doivent être présentés, en spécifiant les documents nécessaires (comme le Détail Quantitatif Estimatif et le Bordereau de Prix Unitaires) sans explication.

6.Délai d’exécution :

ecrire : Les délais d’exécution sont indiqués à l’article[numero de l'article] du CCAP.
7. Sous-traitance :

Extrait les dispositions relatives à la sous-traitance spécifiées dans le CCAP.
Mentionne l'article pertinent du Code de la Commande Publique (articles L. 2193-1 et suivants si existe) relatif à la sous-traitance.
Mentionner seulement et sans autres detailles qu'il  faudra remplir un acte spécial de sous-traitance par sous-traitant.( n'ajouter pas des infos non mentionner dans les documents et les exemples fournits)

8. Paiements :

décrire les modalités de paiement pour le marché public. Voici une explication détaillée :

Paiement par le pouvoir adjudicateur : Le pouvoir adjudicateur, c'est-à-dire l'entité qui a émis l'appel d'offres, effectuera les paiements des sommes dues pour ce marché en créditant le compte bancaire dont le relevé d’identité bancaire (RIB) est annexé au document.

Cas de groupement conjoint : Si le marché est remporté par un groupement conjoint (plusieurs entreprises associées mais agissant séparément), chaque membre du groupement doit fournir son propre RIB pour recevoir les paiements.

Cas de groupement solidaire : Si le marché est remporté par un groupement solidaire (où les membres sont responsables solidairement), un seul RIB est fourni pour un compte unique, qui recevra l'ensemble des paiements.

Paiements aux sous-traitants : Si des sous-traitants sont payés directement, le pouvoir adjudicateur versera les montants dus sur les comptes désignés dans les annexes relatives à la sous-traitance.

En résumé, ce paragraphe précise comment les paiements seront effectués, selon que le marché soit remporté par un seul titulaire, un groupement conjoint, un groupement solidaire, ou qu'il implique des sous-traitants.

9. Garantie :

Recherchez les informations concernant la retenue de garantie ou l'absence de celle-ci ( en cas d'absence ecrit: Le présent marché public ne prévoit pas de retenue de garantie.

).
Mentionne les articles du CCAP relatifs aux garanties applicables au marché public.

10. Échanges dématérialisés :

Identifie les préférences pour les échanges dématérialisés indiquées dans le CCAP.
Extrait l'adresse email du candidat pour les échanges pendant la passation et l'exécution du marché.
Précise la nécessité pour le candidat de tenir le pouvoir adjudicateur informé de toute modification de cette adresse email.
ecrire a la fin de cette partie: Adresse du courrier électronique du candidat à utiliser pour les échanges dématérialisés :
Structure le texte généré de manière claire et conforme au format du Projet Acte d'Engagement. Ce sont des exemples de ces sections {"pae2".join(previous_contexts)}"""

  response = get_response(prompt,600,0.7)

  return response


def generate_all_response(name,cctp,ccap,aapc,rc,name_organisation,pays,num_pub_JOUE,num_avis_JAL_BOAMP,URL_JO,num_et_rue,code_postal,ville,email,num_tlp,perso_contact,type_identifiant,lots_passation_marhe="Pas d'information sur les lots") :
  context = generate_context(name,cctp)
  pub_infos=get_pub_infos(name_organisation,pays,num_pub_JOUE,num_avis_JAL_BOAMP,URL_JO)
  infos_passation=get_infos_passation(context,cctp)
  infos_operateur=get_infos_operateur(num_et_rue,code_postal,ville,pays,email,num_tlp,perso_contact,type_identifiant,lots_passation_marhe="Pas d'information sur les lots")
  infos_represantants=get_infos_represantants()
  capacités=get_capacités_autres_entités_et_sous_traitants()
  section1=generate_PROCEDURE_FORM_OF_PUBLIC_CONTRACT(ccap,aapc)
  sections_4_to_10=generate_sections_4_to_10(ccap,rc)
  final_response  = {
      "context" : context,
      "pub_infos":pub_infos,
      "infos_passation":infos_passation,
      "infos_operateur":infos_operateur,
      "infos_represantants":infos_represantants,
      "capacités":capacités,
      "section1_projetAE":section1,
      "sections_4_to_10_projetAE":sections_4_to_10

  }
  return final_response


