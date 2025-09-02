# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 10:18:01 2025

@author: francois.fabien
"""

import streamlit as st
import pandas as pd

st.title("Ajouter les nombres de ventes aux données")

if st.session_state["df"] is not None:
    st.info("Les données ont bien été initialisées !")
else :
    st.warning("Cette page ne fonctionnera pas correctement tant que les données n'auront pas été initialisées !")
    
dataGlobal = st.session_state["df"]

st.write('Importez un fichier au format xlsx avec le code produit dans une colonne nommée Code produit, et les colonnes que vous voulez à côté.')

uploaded_file = st.file_uploader("Importer les données de vente au format excel", type="xlsx")

if uploaded_file is not None:
    ventes = pd.read_excel(uploaded_file)
    dataMerged = dataGlobal.merge(ventes, on='Code produit', how="left")
    st.session_state["df"] = dataMerged
    st.write("Données de ventes ajoutées !")