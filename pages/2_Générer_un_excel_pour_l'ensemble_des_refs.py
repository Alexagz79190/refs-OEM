# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 10:46:02 2025

@author: francois.fabien
"""

import streamlit as st
import pandas as pd
import re
import numpy as np

nonAlnumRegex = re.compile(r'[^a-zA-Z0-9]+')
fillValues = {"Code produit" : "", "Libellé produit" : "", "Fournisseur : libellé" : "", "Equivalences : références" : "", "Prix d'achat en cours" : 99999}
colonnesObligatoires = list(fillValues.keys())

def traitementDesMerges(listeTexte):
    texte = "|||".join(listeTexte)
    listeTexte = texte.split("|||")
    listeTexteSansDoublons = list(dict.fromkeys(listeTexte))
    return "||".join(filter(None,listeTexteSansDoublons))

def removeNonAlnum(texte):
    return nonAlnumRegex.sub('',str(texte))

def traiterFichier(fichier, sep):
    fichierData = pd.read_excel(uploaded_file)
    fichierData = fichierData.dropna(subset=['ref OEM'])
    fichierData['ref OEM'] = fichierData['ref OEM'].astype(str)
    if sep != "" :
        fichierData['ref OEM'] = fichierData['ref OEM'].str.split("|")
        fichierData = fichierData.dropna(subset=['ref OEM'])
        fichierData = fichierData.explode('ref OEM').reset_index(drop=True)
    fichierData['ref OEM'] = fichierData['ref OEM'].map(lambda x: x.strip())
    fichierData = fichierData.drop_duplicates(subset=['ref produit', 'ref OEM'])
    if matching :
        mergedData = fichierData.merge(dataGlobal, left_on='ref OEM', right_on='Equivalences : références', how="left")
    else :
        fichierData.insert(3,"ref OEM alphanum",fichierData['ref OEM'].map(removeNonAlnum))
        mergedData = fichierData.merge(dataGlobal, on='ref OEM alphanum', how="left")
    mergedData = mergedData.fillna(value = fillValues)
    mergedDataInter = mergedData.copy()
    mergedDataInter["idxmin prix achat"] = mergedDataInter["Prix d'achat en cours"]
    mergedDataInter = mergedDataInter.groupby(["ref produit", "ref OEM", "Nouveau prix d'achat"]).agg({
        "Code produit": lambda x: "|||".join(x),"Libellé produit": lambda x: "|||".join(x), "Fournisseur : libellé": 
            lambda x: "|||".join(x), "Equivalences : références": lambda x: "|||".join(x), "Prix d'achat en cours": 
                'min', 'idxmin prix achat': 'idxmin'}).rename({"Prix d'achat en cours":"Minimum prix d'achat dans le BO"}, axis=1).reset_index()
    resultData = mergedDataInter.copy()
    resultData["idxmin inter prix achat"] = resultData["Minimum prix d'achat dans le BO"]
    resultData = resultData.groupby(["ref produit", "Nouveau prix d'achat"]).agg({
        "ref OEM" : lambda x: "|".join(x), "Code produit": traitementDesMerges,"Libellé produit": traitementDesMerges, "Fournisseur : libellé": 
            traitementDesMerges, "Equivalences : références": traitementDesMerges, "Minimum prix d'achat dans le BO": 
                'min', "idxmin inter prix achat": 'idxmin'}).reset_index()
    resultData.insert(9, "fourn le moins cher", resultData["idxmin inter prix achat"].map(lambda x: mergedData.at[mergedDataInter.at[x, 'idxmin prix achat'],"Fournisseur : libellé"]))
    resultData.insert(10, "Comparaison prix achat", "")
    resultData["Comparaison prix achat"] = np.where(resultData["Nouveau prix d'achat"] < resultData["Minimum prix d'achat dans le BO"], "Nouveau prix d'achat plus bas !", np.where(resultData["Nouveau prix d'achat"] == resultData["Minimum prix d'achat dans le BO"], "Nouveau prix d'achat égal", "Nouveau prix d'achat plus élevé"))
    compteur = 10
    for column in dataGlobal :
        if column not in colonnesObligatoires and column != "ref OEM alphanum" :
            compteur += 1
            resultData.insert(compteur, column, resultData["idxmin inter prix achat"].map(lambda x: mergedData.at[mergedDataInter.at[x, 'idxmin prix achat'],column]))
    resultData = resultData.drop("idxmin inter prix achat", axis=1)
    return resultData.to_csv().encode("utf-8")
        
    
st.title("Comparer des références en masse")

if st.session_state["df"] is not None:
    st.info("Les données ont bien été initialisées !")
else :
    st.warning("Cette page ne fonctionnera pas correctement tant que les données n'auront pas été initialisées !")
    
dataGlobal = st.session_state["df"]

matching = st.checkbox('''Matching exact  
                       Le matching non exact match les OEM en conservant uniquement les lettres et les chiffres.''')

separateur = st.text_input("Séparateur entre 2 refs OEM dans le fichier envoyé (laisser vide si il n'y a qu'une seule ref OEM par ligne)")

with open("modèle import refs constructeur.xlsx", "rb") as file :
    st.download_button(label="Télécharger le fichier modèle", data = file, file_name = "modèle import refs constructeur.xlsx", mime = "application/vnd.openxmlformats-officedocument")

uploaded_file = st.file_uploader("Importer l'export au format excel", type="xlsx")

if uploaded_file is not None:
    csv = traiterFichier(uploaded_file, separateur)
    st.download_button(label="Télécharger le résultat", data = csv, file_name = "refs_constructeurs_résultat.csv", mime = "test/csv")
    