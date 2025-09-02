# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 14:01:49 2025

@author: francois.fabien
"""

import streamlit as st
import pandas as pd
import re
import numpy as np

nonAlnumRegex = re.compile(r'[^a-zA-Z0-9]+')

def removeNonAlnum(texte):
    return nonAlnumRegex.sub('',str(texte))

def creerDataFrame(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df = df.dropna(subset=['Equivalences : références'])
    df['Equivalences : références'] = df['Equivalences : références'].astype(str)
    df['Equivalences : références'] = df['Equivalences : références'].str.split("|")
    df = df.explode('Equivalences : références').reset_index(drop=True)
    df['Equivalences : références'] = df['Equivalences : références'].map(lambda x: x.strip())
    df['Equivalences : références'] = df['Equivalences : références'].replace('', np.nan)
    df = df.dropna(subset=['Equivalences : références'])
    df = df.drop_duplicates(subset=['Code produit', 'Equivalences : références'])
    df.insert(5,"ref OEM alphanum",df['Equivalences : références'].map(removeNonAlnum))
    df["Stocks : quantités"] = df["Stocks : quantités"].where(df["Stocks : stock Agrizone"]==1, 0)
    df["Stocks : quantités"] = df["Stocks : quantités"].map(lambda x: str(x).split("|")[0])
    return df


if "df" not in st.session_state:
    st.session_state["df"] = None

st.title("Comparaison prix d'achat par ref constructeur")

st.write('''
        Faites un export via le back office contenant les colonnes suivantes :\n
            Code Produit\n
            Libellé produit\n
            Fournisseur : libellé\n
            Equivalences : références\n
            Prix d'achat\n
            Stocks : stock Agrizone\n
            Stocks : quantités\n
         
        Vous pouvez exporter l'intégralité des refs du site ou faire une présélection (seulement les refs en ligne, seulement certains fournisseurs etc).\n
        Vous pouvez ajouter des colonnes supplémentaires si vous le désirez, elles apparaitront dans la visualisation ref par ref.\n
        Pour le résultat global de la comparaison en masse, les colonnes supplémentaires correspondront à leur valeur pour le code produit trouvé avec le plus faible prix.
         ''')
         
uploaded_file = st.file_uploader("Importer l'export au format excel", type="xlsx")
if uploaded_file is not None:
    df = creerDataFrame(uploaded_file)
    st.session_state["df"] = df
    
#Display text based on df being initialised or not

if st.session_state["df"] is not None:
    st.info("Données initialisées pour la session, vous pouvez utiliser les autres pages !")
else :
    st.warning("Les autres pages ne fonctionneront pas correctement tant que les données n'auront pas été initialisées !")
