# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 10:45:33 2025

@author: francois.fabien
"""

import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="wide")

nonAlnumRegex = re.compile(r'[^a-zA-Z0-9]+')

st.title("Chercher une référence à comparer")

if st.session_state["df"] is not None:
    st.info("Les données ont bien été initialisées !")
else :
    st.warning("Cette page ne fonctionnera pas correctement tant que les données n'auront pas été initialisées !")

matching = st.checkbox('''Matching exact  
                       Le matching non exact match les OEM en conservant uniquement les lettres et les chiffres.''')
    
ref = st.text_input("Ref cherchée")

if ref != "" : 
    if matching :
        df = st.session_state["df"]
        st.dataframe(df[df['Equivalences : références'] == ref].sort_values(by="Prix d'achat en cours"), width=1500, hide_index=True, column_config={"ref OEM alphanum" : None})
    else :
        df = st.session_state["df"]
        st.dataframe(df[df['ref OEM alphanum'] == nonAlnumRegex.sub('',str(ref))].sort_values(by="Prix d'achat en cours"), width=1500, hide_index=True, column_config={"ref OEM alphanum" : None})