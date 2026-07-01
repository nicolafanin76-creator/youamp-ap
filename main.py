import streamlit as st
import random
import json
import os
from datetime import date
import streamlit.components.v1 as components

# Configurazione della pagina stile Mobile/Centrato con il nome ufficiale
st.set_page_config(page_title="YouAmp", layout="centered")

CACHE_FILE = "youamp_cache.json"

# BANCA DATI METICOLOSA - STRUTTURATA CON SLOT DI CONSUMO ED ESCLUSIONE ERRORI CROSS-MACRO
BANCA_DATI_BASE = {
    # --- CARBOIDRATI ---
    "Riso Basmati": {"P": 8.0, "C": 78.0, "G": 0.8, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali", "slots_default": ["P/C"]},
    "Riso Integrale": {"P": 7.5, "C": 73.0, "G": 1.9, "Kcal": 341, "cat": "Carboidrati", "sub": "Riso e Cereali", "slots_default": ["P/C"]},
    "Riso Soffiato": {"P": 7.0, "C": 80.0, "G": 0.5, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali", "slots_default": ["C", "S"]},
    "Cornflakes": {"P": 7.0, "C": 84.0, "G": 0.8, "Kcal": 370, "cat": "Carboidrati", "sub": "Cereali Colazione", "slots_default": ["C"]},
    "Granola": {"P": 10.0, "C": 65.0, "G": 12.0, "Kcal": 420, "cat": "Carboidrati", "sub": "Cereali Colazione", "slots_default": ["C"]},
    "Fiocchi d'Avena": {"P": 11.0, "C": 60.0, "G": 8.0, "Kcal": 366, "cat": "Carboidrati", "sub": "Cereali Colazione", "slots_default": ["C"]},
    "Pasta di Semola": {"P": 12.5, "C": 71.3, "G": 1.5, "Kcal": 354, "cat": "Carboidrati", "sub": "Pasta", "slots_default": ["P/C"]},
    "Pasta Integrale": {"P": 13.0, "C": 65.0, "G": 2.0, "Kcal": 330, "cat": "Carboidrati", "sub": "Pasta", "slots_default": ["P/C"]},
    "Pasta di Grano Duro": {"P": 13.0, "C": 73.0, "G": 1.5, "Kcal": 355, "cat": "Carboidrati", "sub": "Pasta", "slots_default": ["P/C"]},
    "Cuscus": {"P": 12.8, "C": 72.4, "G": 0.6, "Kcal": 356, "cat": "Carboidrati", "sub": "Riso e Cereali", "slots_default": ["P/C"]},
    "Gallette di Riso": {"P": 7.9, "C": 81.5, "G": 1.1, "Kcal": 371, "cat": "Carboidrati", "sub": "Pane e Sostituti", "slots_default": ["C", "S", "P/C"]},
    "Patate": {"P": 2.1, "C": 17.9, "G": 0.1, "Kcal": 80, "cat": "Carboidrati", "sub": "Tuberi", "slots_default": ["P/C"]},
    "Patate Dolci": {"P": 1.6, "C": 20.0, "G": 0.1, "Kcal": 86, "cat": "Carboidrati", "sub": "Tuberi", "slots_default": ["P/C"]},
    "Rape": {"P": 1.0, "C": 6.0, "G": 0.1, "Kcal": 28, "cat": "Carboidrati", "sub": "Tuberi", "slots_default": ["P/C"]},

    # --- PROTEINE ---
    "Petto di Pollo": {"P": 23.0, "C": 0.0, "G": 0.8, "Kcal": 100, "cat": "Proteine", "sub": "Carne Bianca", "slots_default": ["P/C"]},
    "Fesa di Tacchino": {"P": 24.0, "C": 0.0, "G": 1.2, "Kcal": 107, "cat": "Proteine", "sub": "Carne Bianca", "slots_default": ["S", "P/C"]},
    "Macinato di Pollo": {"P": 21.0, "C": 0.0, "G": 3.0, "Kcal": 111, "cat": "Proteine", "sub": "Carne Bianca", "slots_default": ["P/C"]},
    "Coniglio": {"P": 22.0, "C": 0.0, "G": 5.0, "Kcal": 133, "cat": "Proteine", "sub": "Carne Bianca", "slots_default": ["P/C"]},
    "Macinato di Coniglio": {"P": 22.0, "C": 0.0, "G": 4.5, "Kcal": 128, "cat": "Proteine", "sub": "Carne Bianca", "slots_default": ["P/C"]},
    "Lonza di Maiale": {"P": 22.0, "C": 0.0, "G": 4.0, "Kcal": 124, "cat": "Proteine", "sub": "Carne Rossa", "slots_default": ["P/C"]},
    "Macinato Magro di Manzo": {"P": 21.0, "C": 0.0, "G": 5.0, "Kcal": 129, "cat": "Proteine", "sub": "Carne Rossa", "slots_default": ["P/C"]},
    "Filetto di Manzo": {"P": 20.5, "C": 0.0, "G": 3.5, "Kcal": 114, "cat": "Proteine", "sub": "Carne Rossa", "slots_default": ["P/C"]},
    "Hamburger di Manzo": {"P": 20.0, "C": 0.0, "G": 6.0, "Kcal": 134, "cat": "Proteine", "sub": "Carne Rossa", "slots_default": ["P/C"]},
    "Carne di Cavallo": {"P": 21.5, "C": 0.0, "G": 2.7, "Kcal": 111, "cat": "Proteine", "sub": "Carne Rossa", "slots_default": ["P/C"]},
    "Bacon": {"P": 14.0, "C": 1.0, "G": 35.0, "Kcal": 375, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["P/C"]},
    "Bresaola": {"P": 32.0, "C": 0.0, "G": 2.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["S", "P/C"]},
    "Sfilacci di Manzo": {"P": 31.0, "C": 0.0, "G": 3.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["S", "P/C"]},
    "Sfilacci di Cavallo": {"P": 32.0, "C": 0.0, "G": 2.5, "Kcal": 150, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["S", "P/C"]},
    "Carne Salada": {"P": 23.0, "C": 0.0, "G": 1.5, "Kcal": 105, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["P/C"]},
    "Prosciutto Crudo": {"P": 26.0, "C": 0.0, "G": 10.0, "Kcal": 194, "cat": "Proteine", "sub": "Affettati e Salumi", "slots_default": ["S", "P/C"]},
    "Albume d'Uovo": {"P": 11.0, "C": 0.7, "G": 0.2, "Kcal": 52, "cat": "Proteine", "sub": "Uova", "slots_default": ["C", "S", "P/C"]},
    "Uovo Intero": {"P": 12.4, "C": 0.0, "G": 8.7, "Kcal": 128, "cat": "Proteine", "sub": "Uova", "slots_default": ["C", "P/C"]},
    "Kefir": {"P": 3.4, "C": 4.0, "G": 1.5, "Kcal": 43, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["C", "S"]},
    "Skyr": {"P": 11.0, "C": 3.5, "G": 0.2, "Kcal": 60, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["C", "S"]},
    "Yogurt Greco 0%": {"P": 10.3, "C": 3.0, "G": 0.0, "Kcal": 53, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["C", "S"]},
    "Fiocchi di Latte": {"P": 12.0, "C": 3.0, "G": 4.5, "Kcal": 101, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["S", "P/C"]},
    "Mozzarella Light": {"P": 18.0, "C": 1.0, "G": 9.0, "Kcal": 157, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["P/C"]},
    "Ricotta Light": {"P": 9.0, "C": 4.0, "G": 5.0, "Kcal": 97, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["S", "P/C"]},
    "Feta Greca": {"P": 14.0, "C": 4.0, "G": 21.0, "Kcal": 261, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["P/C"]},
    "Parmigiano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["S", "P/C"]},
    "Grana Padano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["S", "P/C"]},
    "Crema di Riso": {"P": 7.3, "C": 79.0, "G": 1.0, "Kcal": 354, "cat": "Proteine", "sub": "Latticini e Formaggi", "slots_default": ["C"]},
    "Branzino": {"P": 18.5, "C": 0.0, "G": 2.5, "Kcal": 99, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Orata": {"P": 19.8, "C": 0.0, "G": 3.7, "Kcal": 113, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Gamberetti": {"P": 18.5, "C": 0.5, "G": 0.6, "Kcal": 81, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Salmone": {"P": 20.0, "C": 0.0, "G": 13.0, "Kcal": 197, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Trancio di Tonno": {"P": 23.0, "C": 0.0, "G": 1.0, "Kcal": 101, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Trancio di Pesce Spada": {"P": 20.0, "C": 0.0, "G": 4.0, "Kcal": 116, "cat": "Proteine", "sub": "Pesce", "slots_default": ["P/C"]},
    "Tonno al Naturale": {"P": 25.0, "C": 0.0, "G": 0.5, "Kcal": 104, "cat": "Proteine", "sub": "Pesce in Scatola", "slots_default": ["S", "P/C"]},
    "Sgombro in scatola": {"P": 22.0, "C": 0.0, "G": 12.0, "Kcal": 196, "cat": "Proteine", "sub": "Pesce in Scatola", "slots_default": ["S", "P/C"]},

    # --- GRASSI ---
    "Olio Extra Vergine d'Oliva": {"P": 0.0, "C": 0.0, "G": 99.0, "Kcal": 899, "cat": "Grassi", "sub": "Condimenti", "slots_default": ["C", "S", "P/C"]},
    "Noci": {"P": 16.0, "C": 5.5, "G": 65.0, "Kcal": 654, "cat": "Grassi", "sub": "Frutta Secca", "slots_default": ["C", "S"]},
    "Mandorle": {"P": 22.0, "C": 4.6, "G": 50.0, "Kcal": 579, "cat": "Grassi", "sub": "Frutta Secca", "slots_default": ["C", "S"]},
    "Cioccolato Fondente": {"P": 5.0, "C": 50.0, "G": 32.0, "Kcal": 515, "cat": "Grassi", "sub": "Cioccolato e Creme", "slots_default": ["C", "S"]},
    "Burro d'Arachidi": {"P": 25.0, "C": 20.0, "G": 50.0, "Kcal": 588, "cat": "Grassi", "sub": "Burri e Creme", "slots_default": ["C", "S"]},
    "Crema di Mandorle": {"P": 21.0, "C": 19.0, "G": 55.0, "Kcal": 614, "cat": "Grassi", "sub": "Burri e Creme", "slots_default": ["C", "S"]},
    "Hummus": {"P": 5.0, "C": 14.0, "G": 9.0, "Kcal": 166, "cat": "Grassi", "sub": "Salse Fit", "slots_default": ["P/C"]},
    "Guacamole": {"P": 2.0, "C": 8.0, "G": 15.0, "Kcal": 157, "cat": "Grassi", "sub": "Salse Fit", "slots_default": ["P/C"]},
    "Avocado": {"P": 1.9, "C": 8.6, "G": 15.4, "Kcal": 160, "cat": "Grassi", "sub": "Salse Fit", "slots_default": ["C", "S", "P/C"]},

    # --- VERDURE & LEGUMI ---
    "Broccoli": {"P": 2.8, "C": 7.0, "G": 0.4, "Kcal": 34, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Lattuga": {"P": 1.3, "C": 2.2, "G": 0.2, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Rucola": {"P": 2.6, "C": 3.7, "G": 0.7, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Pomodorini": {"P": 1.0, "C": 3.5, "G": 0.2, "Kcal": 18, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Pomodori": {"P": 0.9, "C": 3.9, "G": 0.2, "Kcal": 18, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Peperoni": {"P": 0.9, "C": 4.2, "G": 0.3, "Kcal": 22, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Melanzane": {"P": 1.1, "C": 2.6, "G": 0.1, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Carote": {"P": 1.1, "C": 7.6, "G": 0.2, "Kcal": 35, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Finocchi": {"P": 1.2, "C": 7.3, "G": 0.2, "Kcal": 31, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cavolfiore": {"P": 1.9, "C": 5.0, "G": 0.3, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cetriolo": {"P": 0.6, "C": 3.6, "G": 0.1, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cavolo Cappuccio": {"P": 1.4, "C": 4.3, "G": 0.2, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cicoria": {"P": 1.7, "C": 4.0, "G": 0.3, "Kcal": 23, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Bieta": {"P": 1.8, "C": 3.7, "G": 0.3, "Kcal": 19, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Porro": {"P": 1.5, "C": 14.0, "G": 0.3, "Kcal": 61, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cipolla": {"P": 1.1, "C": 9.3, "G": 0.1, "Kcal": 40, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Sedano": {"P": 0.7, "C": 3.0, "G": 0.2, "Kcal": 16, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Cavolo Nero": {"P": 3.3, "C": 6.0, "G": 0.7, "Kcal": 49, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Zucca": {"P": 1.0, "C": 6.5, "G": 0.1, "Kcal": 26, "cat": "Verdura", "sub": "Zucca", "slots_default": ["P/C"]},
    "Funghi": {"P": 3.1, "C": 3.3, "G": 0.3, "Kcal": 22, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Zucchine": {"P": 1.3, "C": 1.4, "G": 0.1, "Kcal": 11, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Spinaci": {"P": 3.4, "C": 0.6, "G": 0.7, "Kcal": 23, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Fagiolini": {"P": 1.8, "C": 7.0, "G": 0.2, "Kcal": 31, "cat": "Verdura", "sub": "Ortaggi", "slots_default": ["P/C"]},
    "Piselli": {"P": 5.4, "C": 14.5, "G": 0.4, "Kcal": 81, "cat": "Verdura", "sub": "Legumi", "slots_default": ["P/C"]},
    "Fagioli": {"P": 21.0, "C": 50.0, "G": 1.2, "Kcal": 291, "cat": "Verdura", "sub": "Legumi", "slots_default": ["P/C"]},
    "Lenticchie": {"P": 25.0, "C": 54.0, "G": 1.1, "Kcal": 325, "cat": "Verdura", "sub": "Legumi", "slots_default": ["P/C"]},
    "Ceci": {"P": 19.0, "C": 47.0, "G": 6.0, "Kcal": 316, "cat": "Verdura", "sub": "Legumi", "slots_default": ["P/C"]},

    # --- FRUTTA ---
    "Banana": {"P": 1.1, "C": 23.0, "G": 0.3, "Kcal": 89, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C"]},
    "Kiwi": {"P": 1.1, "C": 15.0, "G": 0.5, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Pesca": {"P": 0.8, "C": 9.1, "G": 0.1, "Kcal": 39, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Fragole": {"P": 0.7, "C": 7.7, "G": 0.3, "Kcal": 32, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Frutti Rossi": {"P": 1.0, "C": 12.0, "G": 0.5, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Melone": {"P": 0.8, "C": 7.4, "G": 0.2, "Kcal": 34, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Anguria": {"P": 0.6, "C": 3.7, "G": 0.2, "Kcal": 16, "cat": "Frutta", "sub": "Frutta Dolce", "slots_default": ["C", "S"]},
    "Pera": {"P": 0.3, "C": 15.0, "G": 0.1, "Kcal": 57, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Uva": {"P": 0.7, "C": 15.6, "G": 0.1, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Arancia": {"P": 0.9, "C": 12.0, "G": 0.1, "Kcal": 47, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Clementine": {"P": 0.9, "C": 12.0, "G": 0.1, "Kcal": 47, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Ananas": {"P": 0.5, "C": 13.0, "G": 0.1, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Esotica", "slots_default": ["C", "S"]},
    "Mango": {"P": 0.8, "C": 15.0, "G": 0.4, "Kcal": 60, "cat": "Frutta", "sub": "Frutta Esotica", "slots_default": ["C", "S"]},
    "Cocco": {"P": 3.3, "C": 15.0, "G": 33.0, "Kcal": 354, "cat": "Frutta", "sub": "Frutta Esotica", "slots_default": ["C", "S"]},
    "Albicocche": {"P": 1.4, "C": 11.0, "G": 0.4, "Kcal": 48, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Ciliegie": {"P": 1.0, "C": 16.0, "G": 0.2, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Mela": {"P": 0.3, "C": 14.0, "G": 0.2, "Kcal": 52, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},
    "Macedonia di Frutta": {"P": 0.8, "C": 11.5, "G": 0.2, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Standard", "slots_default": ["C", "S"]},

    # --- SUCCHI & DOLCIFICANTI ---
    "Succo d'Arancia": {"P": 0.7, "C": 10.0, "G": 0.2, "Kcal": 45, "cat": "Frutta", "sub": "Succhi e Bevande", "slots_default": ["C", "S"]},
    "Succhi senza Zucchero": {"P": 0.4, "C": 6.0, "G": 0.1, "Kcal": 28, "cat": "Frutta", "sub": "Succhi e Bevande", "slots_default": ["C", "S"]},
    "Bibite senza Zucchero": {"P": 0.0, "C": 0.1, "G": 0.0, "Kcal": 1, "cat": "Frutta", "sub": "Succhi e Bevande", "slots_default": ["C", "S", "P/C"]},
    "Miele": {"P": 0.6, "C": 80.0, "G": 0.0, "Kcal": 322, "cat": "Dolcificanti", "sub": "Zuccheri Fit", "slots_default": ["C"]},
    "Marmellata senza Zucchero": {"P": 0.5, "C": 25.0, "G": 0.1, "Kcal": 105, "cat": "Dolcificanti", "sub": "Zuccheri Fit", "slots_default": ["C", "S"]},
    "Stevia": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Dolcificanti", "sub": "Zuccheri Fit", "slots_default": ["C", "S", "P/C"]},
    "Dolcificante": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Dolcificanti", "sub": "Zuccheri Fit", "slots_default": ["C", "S", "P/C"]}
}

BANCA_DATI_EXTRA_SORGENTE = {
    # --- PIZZE & PINSE ---
    "Pizza Margherita": {"Kcal": 700, "info": "1 Porzione Media"},
    "Pizza Farcita": {"Kcal": 950, "info": "1 Porzione Media"},
    "Pizza Fritta": {"Kcal": 1100, "info": "1 Pezzo Standard"},
    "Pinsa Farcita": {"Kcal": 750, "info": "1 Porzione Media"},

    # --- PRIMI PIATTI ---
    "Pasta alla Carbonara": {"Kcal": 850, "info": "1 Piatto Ristorante"},
    "Pasta al Ragù": {"Kcal": 650, "info": "1 Piatto Ristorante"},
    "Pasta al Pesto": {"Kcal": 600, "info": "1 Piatto Ristorante"},
    "Pasta al Burro": {"Kcal": 480, "info": "1 Piatto Ristorante"},
    "Pasta all'Olio": {"Kcal": 450, "info": "1 Piatto Ristorante"},
    "Pasta al Tonno": {"Kcal": 580, "info": "1 Piatto Ristorante"},
    "Pasta Fresca Condita": {"Kcal": 700, "info": "1 Piatto Ristorante"},
    "Lasagne": {"Kcal": 800, "info": "1 Porzione Ristorante"},
    "Pasta all'Amatriciana": {"Kcal": 750, "info": "1 Piatto Ristorante"},
    "Orecchiette alle Cime di Rapa": {"Kcal": 550, "info": "1 Piatto Ristorante"},
    "Risotto (Condito)": {"Kcal": 600, "info": "1 Piatto Ristorante"},
    "Insalata di Riso": {"Kcal": 550, "info": "1 Porzione Media"},
    "Tortellini in Brodo": {"Kcal": 420, "info": "1 Piatto Ristorante"},
    "Tortellini Panna e Prosciutto": {"Kcal": 780, "info": "1 Piatto Ristorante"},
    "Gnocchi ai Formaggi": {"Kcal": 820, "info": "1 Piatto Ristorante"},
    "Tortellini Ripieni": {"Kcal": 500, "info": "1 Porzione Standard"},

    # --- PANE, PIADINE & SNACK ---
    "Pane all'Olio": {"Kcal": 310, "info": "100g standard"},
    "Grissini": {"Kcal": 410, "info": "100g standard"},
    "Taralli": {"Kcal": 460, "info": "100g standard"},
    "Piadina Farcita": {"Kcal": 700, "info": "1 Porzione Standard"},
    "Panino Fastfood": {"Kcal": 650, "info": "1 Singolo Hamburger Completo"},

    # --- SECONDI DI CARNE ---
    "Carne di Agnello": {"Kcal": 480, "info": "1 Porzione Standard 200g"},
    "Polpette": {"Kcal": 380, "info": "1 Porzione Standard 4 pezzi"},
    "Polpette al Sugo": {"Kcal": 460, "info": "1 Porzione Ristorante"},
    "Carne di Maiale alla Griglia": {"Kcal": 450, "info": "1 Porzione Standard"},
    "Carne alla Griglia Mista": {"Kcal": 750, "info": "1 Porzione Ristorante"},
    "Tagliata": {"Kcal": 420, "info": "1 Porzione 250g"},
    "Affettati di Maiale": {"Kcal": 320, "info": "1 Tagliere misto 100g"},
    "Formaggi": {"Kcal": 380, "info": "1 Porzione Mista 100g"},
    "Spezzatino": {"Kcal": 520, "info": "1 Porzione Standard"},
    "Polenta": {"Kcal": 250, "info": "1 Porzione Standard 150g"},
    "Coniglio Arrosto": {"Kcal": 380, "info": "1 Porzione Standard"},
    "Arrosto di Maiale": {"Kcal": 410, "info": "1 Porzione Standard"},
    "Arrosto di Vitello": {"Kcal": 350, "info": "1 Porzione Standard"},
    "Caprese": {"Kcal": 320, "info": "1 Porzione Standard"},
    "Ragù d'Anatra": {"Kcal": 350, "info": "1 Porzione da Condimento"},
    "Trippa": {"Kcal": 280, "info": "1 Porzione Ristorante"},
    "Cotechino": {"Kcal": 450, "info": "1 Porzione 100g"},
    "Carne Bollita di Manzo": {"Kcal": 310, "info": "1 Porzione Standard"},
    "Carne Bollita di Pollo": {"Kcal": 220, "info": "1 Porzione Standard"},
    "Cappone": {"Kcal": 340, "info": "1 Porzione Standard"},
    "Scaloppa ai Funghi": {"Kcal": 420, "info": "1 Porzione Standard"},
    "Scaloppa al Limone": {"Kcal": 380, "info": "1 Porzione Standard"},
    "Scaloppa alle Verdure": {"Kcal": 390, "info": "1 Porzione Standard"},
    "Cotoletta": {"Kcal": 550, "info": "1 Pezzo Standard"},
    "Würstel": {"Kcal": 270, "info": "1 Porzione 100g"},
    "Filetto Lardellato": {"Kcal": 480, "info": "1 Porzione Standard"},
    "Anatra al Forno": {"Kcal": 460, "info": "1 Porzione Standard"},

    # --- FRITTI, CONTORNI & VERDURE SOCIAL ---
    "Melanzane Fritte": {"Kcal": 290, "info": "1 Porzione 150g"},
    "Parmigiana di Melanzane": {"Kcal": 580, "info": "1 Porzione Abbondante"},
    "Caponata": {"Kcal": 240, "info": "1 Porzione Standard"},
    "Mozzarella in Carrozza": {"Kcal": 480, "info": "1 Pezzo Grande"},
    "Mozzarelline Fritte": {"Kcal": 340, "info": "1 Porzione 6 pezzi"},
    "Crocchette di Patate": {"Kcal": 280, "info": "1 Porzione 3 pezzi"},
    "Patate al Forno": {"Kcal": 220, "info": "1 Porzione Media"},

    # --- SECONDI DI PESCE & ETNICO ---
    "Rombo al Forno": {"Kcal": 310, "info": "1 Filetto Ristorante"},
    "Sushi": {"Kcal": 450, "info": "Set Misto Combinato 8 pezzi"},
    "Baccalà Mantecato": {"Kcal": 350, "info": "1 Porzione 100g"},
    "Baccalà alla Vicentina": {"Kcal": 490, "info": "1 Porzione Ristorante"},
    "Polpo": {"Kcal": 180, "info": "1 Porzione Standard Insalata"},
    "Seppia": {"Kcal": 200, "info": "1 Porzione Umido/Griglia"},
    "Spaghetti allo Scoglio": {"Kcal": 650, "info": "1 Piatto Ristorante"},
    "Spaghetti alle Cozze": {"Kcal": 580, "info": "1 Piatto Ristorante"},
    "Spaghetti alle Vongole": {"Kcal": 550, "info": "1 Piatto Ristorante"},
    "Frittura Mista di Pesce": {"Kcal": 600, "info": "1 Porzione Media"},
    "Risotto Nero di Seppia": {"Kcal": 590, "info": "1 Piatto Ristorante"},
    "Risotto di Pesce": {"Kcal": 610, "info": "1 Piatto Ristorante"},
    "Scampi": {"Kcal": 120, "info": "1 Porzione Griglia 150g"},
    "Gamberoni": {"Kcal": 140, "info": "1 Porzione Griglia 150g"},
    "Totani": {"Kcal": 220, "info": "1 Porzione Umido/Griglia"},
    "Mazzancolle": {"Kcal": 130, "info": "1 Porzione Standard"},
    "Capasanta Gratinata": {"Kcal": 180, "info": "2 Pezzi"},

    # --- COLAZIONE & BAR ---
    "Croissant Integrale": {"Kcal": 260, "info": "1 Pezzo Standard"},
    "Croissant Farcito": {"Kcal": 360, "info": "1 Pezzo Standard"},
    "Cappuccino": {"Kcal": 110, "info": "1 Tazza Standard Intero"},
    "Cioccolata Calda": {"Kcal": 280, "info": "1 Tazza Standard"},
    "Krapfen Farcito": {"Kcal": 420, "info": "1 Pezzo Grande"},
    "Frittelle": {"Kcal": 290, "info": "1 Porzione 100g"},
    "Frittelle Farcite": {"Kcal": 390, "info": "1 Porzione 100g"},
    "Brioche Confezionate": {"Kcal": 210, "info": "1 Merendina Standard"},

    # --- PASTICCERIA & DOLCI EXTRA ---
    "Gelato Artigianale": {"Kcal": 250, "info": "1 Coppetta Media"},
    "Gelato Confezionato": {"Kcal": 180, "info": "1 Pezzo su Stecco o Cono"},
    "Cheesecake": {"Kcal": 450, "info": "1 Fetta Standard"},
    "Tiramisù": {"Kcal": 480, "info": "1 Porzione Standard"},
    "Torta di Frutta": {"Kcal": 350, "info": "1 Fetta Standard"},
    "Meringata": {"Kcal": 400, "info": "1 Fetta Standard"},
    "Sorbetto": {"Kcal": 150, "info": "1 Bicchiere"},
    "Sorbetto al Limone": {"Kcal": 150, "info": "1 Bicchiere"},
    "Panettone": {"Kcal": 370, "info": "1 Fetta 100g"},
    "Pandoro": {"Kcal": 410, "info": "1 Fetta 100g"},
    "Torta di Mele": {"Kcal": 320, "info": "1 Fetta Standard"},
    "Millefoglie": {"Kcal": 460, "info": "1 Fetta Standard"},
    "Nutella": {"Kcal": 81, "info": "1 Cucchiaino 15g"},
    "Marmellata": {"Kcal": 38, "info": "1 Cucchiaino 15g"},
    "Uvetta": {"Kcal": 45, "info": "1 Cucchiaio 15g"},
    "Cioccolato al Latte": {"Kcal": 270, "info": "Mezza Barretta 50g"},

    # --- ALCOLICI & BEVANDE EXTRA ---
    "Birra": {"Kcal": 150, "info": "1 Lattina/Bottiglia 33cl"},
    "Bibita Gassata Dolce": {"Kcal": 130, "info": "1 Lattina 33cl"},
    "The Zuccherati": {"Kcal": 110, "info": "1 Bicchiere/Lattina"},
    "Succo di Frutta": {"Kcal": 120, "info": "1 Bicchiere Standard"},
    "Gin Tonic": {"Kcal": 170, "info": "1 Bicchiere Standard"},
    "Spritz Aperol": {"Kcal": 140, "info": "1 Bicchiere Standard"},
    "Spritz Misto": {"Kcal": 120, "info": "1 Bicchiere Standard"},
    "Calice di Prosecco": {"Kcal": 90, "info": "1 Calice Standard"},
    "Calice di Vino Rosso": {"Kcal": 100, "info": "1 Calice Standard"},
    "Calice di Vino Bianco": {"Kcal": 95, "info": "1 Calice Standard"},
    "Vodka": {"Kcal": 115, "info": "1 Shot 50ml"},
    "Mojito": {"Kcal": 180, "info": "1 Bicchiere Standard"}
}

DATABASE_EXTRA_UNIFICATO = {}
for k, v in BANCA_DATI_EXTRA_SORGENTE.items():
    DATABASE_EXTRA_UNIFICATO[k] = {"Kcal": v["Kcal"], "info": v["info"]}
for k, v in BANCA_DATI_BASE.items():
    DATABASE_EXTRA_UNIFICATO[f"{k} (Porzione da 100g)"] = {"Kcal": v["Kcal"], "info": "100g standard"}

# --- LOGICA DI SALVATAGGIO E RIPRISTINO PERMANENTE (CACHE JSON) ---
def carica_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salva_cache():
    dati = {
        "acqua_bevuta": st.session_state.get("acqua_bevuta", 0.0),
        "pasti_generati": st.session_state.get("pasti_generati", {}),
        "piani_integratori": st.session_state.get("piani_integratori", {}),
        "cal_generate_wo": st.session_state.get("cal_generate_wo", 0.0),
        "cal_generate_rest": st.session_state.get("cal_generate_rest", 0.0),
        "app_salute_wo": st.session_state.get("app_salute_wo", 3500.0),
        "app_salute_rest": st.session_state.get("app_salute_rest", 2200.0),
        "dispensa_slots": st.session_state.get("dispensa_slots", {}),
        "pt_kcal_wo": st.session_state.get("pt_kcal_wo", 3346),
        "spesa_wo": st.session_state.get("spesa_wo", 3500),
        "pt_kcal_rest": st.session_state.get("pt_kcal_rest", 2500),
        "spesa_rest": st.session_state.get("spesa_rest", 2200),
        "target_acqua_manuale": st.session_state.get("target_acqua_manuale", 4.0),
        "macro_wo_pasti": st.session_state.get("macro_wo_pasti", {}),
        "macro_rest_pasti": st.session_state.get("macro_rest_pasti", {}),
        "peso_corrente": st.session_state.get("peso_corrente", 91.6),
        "ore_sonno": st.session_state.get("ore_sonno", 8.0),
        "passi": st.session_state.get("passi", 10000),
        "km_percorsi": st.session_state.get("km_percorsi", 7.2),
        "fc_media": st.session_state.get("fc_media", 68),
        "data_nascita_str": str(st.session_state.get("data_nascita_val", "2000-01-01"))
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

cache_iniziale = carica_cache()

# Inizializzazione controllata con ripristino da cache
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = cache_iniziale.get("acqua_bevuta", 0.0)
if "pasti_generati" not in st.session_state:
    pg = cache_iniziale.get("pasti_generati", {})
    st.session_state.pasti_generati = {int(k): v for k, v in pg.items()}
if "piani_integratori" not in st.session_state:
    pi = cache_iniziale.get("piani_integratori", {})
    st.session_state.piani_integratori = {int(k): v for k, v in pi.items()}
if "extra_temporanei" not in st.session_state:
    st.session_state.extra_temporanei = {}
if "cal_generate_wo" not in st.session_state:
    st.session_state.cal_generate_wo = cache_iniziale.get("cal_generate_wo", 0.0)
if "cal_generate_rest" not in st.session_state:
    st.session_state.cal_generate_rest = cache_iniziale.get("cal_generate_rest", 0.0)
if "app_salute_wo" not in st.session_state:
    st.session_state.app_salute_wo = cache_iniziale.get("app_salute_wo", 3500.0)
if "app_salute_rest" not in st.session_state:
    st.session_state.app_salute_rest = cache_iniziale.get("app_salute_rest", 2200.0)
if "dispensa_slots" not in st.session_state:
    st.session_state.dispensa_slots = cache_iniziale.get("dispensa_slots", {})

if "peso_corrente" not in st.session_state:
    st.session_state.peso_corrente = cache_iniziale.get("peso_corrente", 91.6)
if "ore_sonno" not in st.session_state:
    st.session_state.ore_sonno = cache_iniziale.get("ore_sonno", 8.0)
if "passi" not in st.session_state:
    st.session_state.passi = cache_iniziale.get("passi", 10000)
if "km_percorsi" not in st.session_state:
    st.session_state.km_percorsi = cache_iniziale.get("km_percorsi", 7.2)
if "fc_media" not in st.session_state:
    st.session_state.fc_media = cache_iniziale.get("fc_media", 68)

if "macro_wo_pasti" not in st.session_state:
    mwp = cache_iniziale.get("macro_wo_pasti", {})
    if mwp:
        st.session_state.macro_wo_pasti = {int(k): v for k, v in mwp.items()}
    else:
        st.session_state.macro_wo_pasti = {i: {"P": 40, "C": 50, "G": 10} for i in range(1, 8)}

if "macro_rest_pasti" not in st.session_state:
    mrp = cache_iniziale.get("macro_rest_pasti", {})
    if mrp:
        st.session_state.macro_rest_pasti = {int(k): v for k, v in mrp.items()}
    else:
        st.session_state.macro_rest_pasti = {i: {"P": 40, "C": 30, "G": 15} for i in range(1, 8)}

# CSS Nativo Antioscillazione Rigido
pwa_html = """
<style>
    .stMarkdown, .stButton, .stToggle, .stMetric, h1, h2, h3 {
        text-align: center !important;
        justify-content: center !important;
    }
    div[data-testid="stMetricValue"] {
        text-align: center !important;
    }
    div[data-testid="stBlock"] {
        text-align: center !important;
    }
    html, body {
        overflow-x: hidden !important;
        max-width: 100% !important;
    }
</style>
"""
st.markdown(pwa_html, unsafe_allow_html=True)

# --- INTERFACCIA SINISTRA: SIDEBAR ---
st.sidebar.title("Profilo e Impostazioni")

foto_profilo = st.sidebar.file_uploader("Carica la tua foto profilo:", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
if foto_profilo is not None:
    st.sidebar.image(foto_profilo, width=120)

nome_atleta = st.sidebar.text_input("Nome Atleta:", value="Nicola Fanin")
altezza = st.sidebar.number_input("Altezza (cm):", min_value=100, max_value=250, value=190)

dn_cached_str = cache_iniziale.get("data_nascita_str", "2000-01-01")
try:
    dn_parsed = date.fromisoformat(dn_cached_str)
except:
    dn_parsed = date(2000, 1, 1)
data_nascita_input = st.sidebar.date_input("Data di Nascita:", value=dn_parsed, min_value=date(1920, 1, 1), max_value=date(2026, 12, 31), key="data_nascita_val")
eta = 2026 - data_nascita_input.year - ((6, 30) < (data_nascita_input.month, data_nascita_input.day))

st.sidebar.write("---")
st.sidebar.subheader("Fabbisogno e consumo calorico consigliato")

col_wo1, col_wo2 = st.sidebar.columns(2)
with col_wo1:
    pt_kcal_wo = col_wo1.number_input("Fabbisogno WO (Kcal)", value=cache_iniziale.get("pt_kcal_wo", 3346), key="pt_kcal_wo")
with col_wo2:
    spesa_prevista_wo = col_wo2.number_input("Consumo Stimato WO (Kcal)", value=cache_iniziale.get("spesa_wo", 3500), key="spesa_wo")

col_rst1, col_rst2 = st.sidebar.columns(2)
with col_rst1:
    pt_kcal_rest = col_rst1.number_input("Fabbisogno REST (Kcal)", value=cache_iniziale.get("pt_kcal_rest", 2500), key="pt_kcal_rest")
with col_rst2:
    spesa_prevista_rest = col_rst2.number_input("Consumo Stimato REST (Kcal)", value=cache_iniziale.get("spesa_rest", 2200), key="spesa_rest")

st.sidebar.write("---")
st.sidebar.subheader("Target Idrico Specifico")
target_acqua_manuale = st.sidebar.number_input("Indicazione Acqua (Litri)", value=cache_iniziale.get("target_acqua_manuale", 4.0), key="target_acqua_manuale", step=0.5)

st.sidebar.write("---")
st.sidebar.subheader("Dispensa Alimenti")
dispensa_attiva = {}
categorie_lista = ["Carboidrati", "Proteine", "Grassi", "Verdura", "Frutta", "Dolcificanti"]

for categoria in categorie_lista:
    with st.sidebar.expander(categoria.upper()):
        cibi_in_cat = {k: v for k, v in BANCA_DATI_BASE.items() if v["cat"] == categoria}
        sottotipi = sorted(list(set([v["sub"] for v in cibi_in_cat.values()])))
        for sub in sottotipi:
            st.markdown(f"**-- {sub} --**")
            cibi_in_sub = {k: v for k, v in cibi_in_cat.items() if v["sub"] == sub}
            for cibo in cibi_in_sub.keys():
                default_slots = st.session_state.dispensa_slots.get(cibo, BANCA_DATI_BASE[cibo]["slots_default"])
                scelte_utente = st.multiselect(f"{cibo}", options=["C", "S", "P/C"], default=default_slots, key=f"slots_{cibo}")
                st.session_state.dispensa_slots[cibo] = scelte_utente

st.sidebar.write("---")
st.sidebar.subheader("Dispensa Integratori")
lista_integratori = [
    "Proteine ISO", "Proteine Whey", "Creatina", "Carnitina", "Zinco", 
    "Magnesio", "Cromo", "Vitamina D", "Vitamina C", "Vitamina B", 
    "Berberina", "Olio di pesce capsule", "Elettroliti per acqua", 
    "Potassio", "Aminoacidi essenziali", "Aminoacidi ramificati"
]
integratori_attivi = {}
with st.sidebar.expander("INTEGRATORI DISPONIBILI"):
    for ing in lista_integratori:
        default_ing = ing in ["Creatina", "Olio di pesce capsule", "Proteine ISO", "Proteine Whey"]
        integratori_attivi[ing] = st.checkbox(ing, value=default_ing, key=f"ing_{ing}")

st.sidebar.write("---")
st.sidebar.subheader("Dispensa Extra")
dispensa_extra_attiva = {}
with st.sidebar.expander("ALIMENTI EXTRA SOCIAL"):
    for cibo_ex in BANCA_DATI_EXTRA_SORGENTE.keys():
        dispensa_extra_attiva[cibo_ex] = st.checkbox(cibo_ex, value=True, key=f"disp_ex_{cibo_ex}")

st.sidebar.write("---")
st.sidebar.subheader("Configurazione Avanzata Macro Pasti")

with st.sidebar.expander("GIORNI WORKOUT - MACRO PASTI"):
    for i in range(1, 8):
        st.markdown(f"**Pasto {i} (Workout)**")
        st.session_state.macro_wo_pasti[i]["P"] = st.number_input(f"Proteine (g) - P{i} WO", value=st.session_state.macro_wo_pasti[i]["P"], key=f"p_wo_{i}")
        st.session_state.macro_wo_pasti[i]["C"] = st.number_input(f"Carboidrati (g) - P{i} WO", value=st.session_state.macro_wo_pasti[i]["C"], key=f"c_wo_{i}")
        st.session_state.macro_wo_pasti[i]["G"] = st.number_input(f"Grassi (g) - P{i} WO", value=st.session_state.macro_wo_pasti[i]["G"], key=f"g_wo_{i}")

with st.sidebar.expander("GIORNI REST - MACRO PASTI"):
    for i in range(1, 8):
        st.markdown(f"**Pasto {i} (Rest)**")
        st.session_state.macro_rest_pasti[i]["P"] = st.number_input(f"Proteine (g) - P{i} REST", value=st.session_state.macro_rest_pasti[i]["P"], key=f"p_rst_{i}")
        st.session_state.macro_rest_pasti[i]["C"] = st.number_input(f"Carboidrati (g) - P{i} REST", value=st.session_state.macro_rest_pasti[i]["C"], key=f"c_rst_{i}")
        st.session_state.macro_rest_pasti[i]["G"] = st.number_input(f"Grassi (g) - P{i} REST", value=st.session_state.macro_rest_pasti[i]["G"], key=f"g_rst_{i}")

st.sidebar.write("---")
if st.sidebar.button("Salva Configurazione Permanente", use_container_width=True):
    salva_cache()
    components.html("""<script>window.parent.document.querySelector('.stSidebar [data-testid="collapsedControl"]').click();</script>""", height=0, width=0)
    st.rerun()


# --- SCHERMATA PRINCIPALE (CENTRATA) ---
st.markdown("<h1>YouAmp</h1>", unsafe_allow_html=True)
st.write("---")

col_toggle = st.columns([1, 2, 1])
with col_toggle[1]:
    giorno_workout = st.toggle("Seleziona Regime Giornaliero", value=True)

if giorno_workout:
    regime_testo = "WORKOUT"
    macro_selezionati_sistema = st.session_state.macro_wo_pasti
else:
    regime_testo = "REST"
    macro_selezionati_sistema = st.session_state.macro_rest_pasti

st.markdown(f"<h2>{regime_testo}</h2>", unsafe_allow_html=True)

st.markdown("<h3>Simulatore Sincronizzazione App Connesse</h3>", unsafe_allow_html=True)
col_sal1, col_sal2 = st.columns(2)
with col_sal1:
    st.session_state.app_salute_wo = st.number_input("Kcal Consumate Rilevate App (Giorno WO)", value=st.session_state.app_salute_wo, step=50.0, on_change=salva_cache)
with col_sal2:
    st.session_state.app_salute_rest = st.number_input("Kcal Consumate Rilevate App (Giorno REST)", value=st.session_state.app_salute_rest, step=50.0, on_change=salva_cache)

deficit_wo = st.session_state.cal_generate_wo - st.session_state.app_salute_wo
deficit_rest = st.session_state.cal_generate_rest - st.session_state.app_salute_rest

st.markdown("<h3>Quadro Energetico Generale</h3>", unsafe_allow_html=True)

stile_griglia = """
<style>
    .quadro-tabella {
        width: 100%;
        max-width: 600px;
        margin: 15px auto !important;
        border-collapse: collapse;
        font-size: 13px !important;
        font-family: sans-serif;
        text-align: center;
        background-color: #FFFFFF !important;
        table-layout: fixed;
    }
    .quadro-tabella th {
        background-color: #F0F2F6 !important;
        color: #111111 !important;
        font-weight: bold;
        padding: 8px !important;
        border: 1px solid #CCCCCC !important;
    }
    .quadro-tabella td {
        padding: 8px !important;
        border: 1px solid #CCCCCC !important;
        color: #111111 !important;
        word-wrap: break-word;
    }
    .quadro-tabella tr:nth-of-type(even) {
        background-color: #F8F9FA !important;
    }
    .quadro-tabella tr:nth-of-type(odd) {
        background-color: #FFFFFF !important;
    }
    .riga-attiva {
        border: 3px solid #00D26A !important;
    }
    .tag-attivo {
        color: #00D26A !important;
        font-weight: bold;
    }
</style>
"""
st.markdown(stile_griglia, unsafe_allow_html=True)

valore_wo_stringa = f"+{round(deficit_wo)}" if deficit_wo > 0 else f"{round(deficit_wo)}"
valore_rest_stringa = f"+{round(deficit_rest)}" if deficit_rest > 0 else f"{round(deficit_rest)}"

html_tabella = f"""
<table class="quadro-tabella">
    <thead>
        <tr>
            <th style="width: 15%;">Regime</th>
            <th style="width: 17%;">Fabbisogno PT</th>
            <th style="width: 18%;">Consumo Stimato PT</th>
            <th style="width: 17%;">Calorie Pasti</th>
            <th style="width: 18%;">Consumo Reale App</th>
            <th style="width: 15%;">Deficit Reale</th>
        </tr>
    </thead>
    <tbody>
        <tr class="{'riga-attiva' if giorno_workout else ''}">
            <td><span class="{'tag-attivo' if giorno_workout else ''}">WO {'•' if giorno_workout else ''}</span></td>
            <td>{pt_kcal_wo}</td>
            <td>{spesa_prevista_wo}</td>
            <td>{round(st.session_state.cal_generate_wo)}</td>
            <td>{round(st.session_state.app_salute_wo)}</td>
            <td>{valore_wo_stringa}</td>
        </tr>
        <tr class="{'riga-attiva' if not giorno_workout else ''}">
            <td><span class="{'tag-attivo' if not giorno_workout else ''}">REST {'•' if not giorno_workout else ''}</span></td>
            <td>{pt_kcal_rest}</td>
            <td>{spesa_prevista_rest}</td>
            <td>{round(st.session_state.cal_generate_rest)}</td>
            <td>{round(st.session_state.app_salute_rest)}</td>
            <td>{valore_rest_stringa}</td>
        </tr>
    </tbody>
</table>
"""
st.markdown(html_tabella, unsafe_allow_html=True)

st.write("---")

# --- SEZIONE INTEGRATORI PERMANENTI INTERATTIVA ---
st.markdown("<h3>Pianificatore Integratori Permanenti</h3>", unsafe_allow_html=True)
integratori_selezionabili = [k for k, v in integratori_attivi.items() if v]

if integratori_selezionabili:
    col_int1, col_int2, col_int3 = st.columns([2, 1, 1])
    with col_int1:
        integratore_scelto = st.selectbox("Seleziona Integratore Attivo", integratori_selezionabili, label_visibility="collapsed")
    with col_int2:
        pasto_destinazione = st.selectbox("Assegna a:", [f"Pasto {i}" for i in range(1, 8)], label_visibility="collapsed")
    with col_int3:
        if st.button("Abbinamento Permanente", use_container_width=True):
            p_id = int(pasto_destinazione.split()[-1])
            if p_id not in st.session_state.piani_integratori:
                st.session_state.piani_integratori[p_id] = []
            if integratore_scelto not in st.session_state.piani_integratori[p_id]:
                st.session_state.piani_integratori[p_id].append(integratore_scelto)
                salva_cache()
                st.rerun()
    if st.session_state.piani_integratori:
        if st.button("Svuota Piano Integratori Memoria", use_container_width=True, type="secondary"):
            st.session_state.piani_integratori = {}
            salva_cache()
            st.rerun()
else:
    st.info("Attiva gli integratori nelle impostazioni (⚙️) per abbinarli.")

st.write("---")

# --- INSERIMENTO PARAMETRI FISICI GIORNALIERI (PERSISTENTI) ---
st.markdown("<h3>Inserimento Parametri Giornalieri</h3>", unsafe_allow_html=True)
col_input1, col_input2, col_input3 = st.columns(3)
with col_input1:
    st.session_state.peso_corrente = st.number_input("Peso di Oggi (Kg)", value=st.session_state.peso_corrente, step=0.1, on_change=salva_cache)
    st.session_state.ore_sonno = st.number_input("Ore di Somno", value=st.session_state.ore_sonno, step=0.5, on_change=salva_cache)
with col_input2:
    st.session_state.passi = st.number_input("Passi Effettuati", value=st.session_state.passi, step=500, on_change=salva_cache)
    st.session_state.km_percorsi = st.number_input("Distanza (Km)", value=st.session_state.km_percorsi, step=0.1, on_change=salva_cache)
with col_input3:
    st.session_state.fc_media = st.number_input("Frequenza Cardiaca (BPM)", value=st.session_state.fc_media, step=1, on_change=salva_cache)

st.write("---")

# Monitoraggio Idratazione
st.markdown("<h3>Monitoraggio Idratazione</h3>", unsafe_allow_html=True)
if st.session_state.acqua_bevuta < target_acqua_manuale:
    st.markdown(f"<h3>Bevuti: {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3>Target Raggiunto! {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L</h3>", unsafe_allow_html=True)

col_w_btn = st.columns([1, 1, 1, 1, 1, 1])
with col_w_btn[1]:
    if st.button("+50ml"): 
        st.session_state.acqua_bevuta += 0.05
        salva_cache()
        st.rerun()
with col_w_btn[2]:
    if st.button("+250ml"): 
        st.session_state.acqua_bevuta += 0.25
        salva_cache()
        st.rerun()
with col_w_btn[3]:
    if st.button("+500ml"): 
        st.session_state.acqua_bevuta += 0.50
        salva_cache()
        st.rerun()
with col_w_btn[4]:
    if st.button("Reset"): 
        st.session_state.acqua_bevuta = 0.0
        salva_cache()
        st.rerun()

st.write("---")

def genera_singolo_pasto_intelligente(target_p, target_c, target_g, pasto_id):
    if pasto_id == 1:
        tag_cercato = "C"
    elif pasto_id in [2, 4, 6, 7]:
        tag_cercato = "S"
    else:
        tag_cercato = "P/C"

    carb_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Carboidrati" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    prot_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Proteine" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    grassi_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Grassi" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    
    fonte_c = random.choice(carb_selezionati) if carb_selezionati else "Gallette di Riso"
    fonte_p = random.choice(prot_selezionati) if prot_selezionati else "Yogurt Greco 0%"
    fonte_g = random.choice(grassi_selezionati) if grassi_selezionati else "Olio Extra Vergine d'Oliva"

    c_purezza = BANCA_DATI_BASE[fonte_c]["C"] / 100.0
    gr_c = round(target_c / c_purezza) if c_purezza > 0 else 0
    
    p_ombra_c = gr_c * (BANCA_DATI_BASE[fonte_c]["P"] / 100.0)
    g_ombra_c = gr_c * (BANCA_DATI_BASE[fonte_c]["G"] / 100.0)

    target_p_rimanente = max(0.0, target_p - p_ombra_c)
    p_purezza = BANCA_DATI_BASE[fonte_p]["P"] / 100.0
    gr_p = round(target_p_rimanente / p_purezza) if p_purezza > 0 else 0

    g_ombra_p = gr_p * (BANCA_DATI_BASE[fonte_p]["G"] / 100.0)

    target_g_rimanente = max(0.0, target_g - g_ombra_c - g_ombra_p)
    g_purezza = BANCA_DATI_BASE[fonte_g]["G"] / 100.0
    gr_g = round(target_g_rimanente / g_purezza) if g_purezza > 0 else 0

    kcal_c = gr_c * (BANCA_DATI_BASE[fonte_c]["Kcal"] / 100.0)
    kcal_p = gr_p * (BANCA_DATI_BASE[fonte_p]["Kcal"] / 100.0)
    kcal_g = gr_g * (BANCA_DATI_BASE[fonte_g]["Kcal"] / 100.0)
    totale_kcal_pasto = kcal_c + kcal_p + kcal_g

    return [
        {"alimento": fonte_c, "grammi": gr_c, "macro": f"C: {target_c}g", "kcal": kcal_c, "target_orig": target_p, "tipo_cat": "Carboidrati"},
        {"alimento": fonte_p, "grammi": gr_p, "macro": f"P: {target_p}g", "kcal": kcal_p, "target_orig": target_p, "tipo_cat": "Proteine"},
        {"alimento": fonte_g, "grammi": gr_g, "macro": f"G: {target_g}g", "kcal": kcal_g, "target_orig": target_p, "tipo_cat": "Grassi"}
    ], totale_kcal_pasto

st.markdown("<h3>Pianificazione Alimentare Giornaliera</h3>", unsafe_allow_html=True)
numero_pasti_main = st.slider("Seleziona numero di pasti giornalieri:", min_value=1, max_value=7, value=5, key="pasti_main")

if st.button("Genera Tutti i Pasti", use_container_width=True, type="primary"):
    st.session_state.pasti_generati = {}
    totale_kcal_giornaliero = 0.0
    
    for idx in range(1, numero_pasti_main + 1):
        target = macro_selezionati_sistema.get(idx, {"P": 40, "C": 50, "G": 10})
        pasto_creato, kcal_pasto = genera_singolo_pasto_intelligente(target["P"], target["C"], target["G"], idx)
        st.session_state.pasti_generati[idx] = pasto_creato
        totale_kcal_giornaliero += kcal_pasto
    
    if giorno_workout:
        st.session_state.cal_generate_wo = totale_kcal_giornaliero
    else:
        st.session_state.cal_generate_rest = totale_kcal_giornaliero
    salva_cache()
    st.rerun()

for idx in range(1, numero_pasti_main + 1):
    if idx == 1:
        tipo_nome_etichetta = "Colazione"
    elif idx in [2, 4, 6, 7]:
        tipo_nome_etichetta = "Spuntino"
    else:
        tipo_nome_etichetta = "Pranzo/Cena"

    kcal_del_pasto_corrente = 0.0
    if idx in st.session_state.pasti_generati:
        kcal_del_pasto_corrente = sum(ing.get("kcal", 0.0) for ing in st.session_state.pasti_generati[idx])

    st.markdown(f"#### Pasto {idx} - {tipo_nome_etichetta} ({round(kcal_del_pasto_corrente)} Kcal)")
    col_pasto_sx, col_pasto_dx = st.columns([2, 1])
    
    with col_pasto_dx:
        riferimento = st.selectbox("Seleziona Tipo", ["Usa Impostazioni", "Workout", "Rest", "Extra"], key=f"ref_{idx}", label_visibility="collapsed")
    
    with col_pasto_sx:
        if riferimento == "Extra":
            if idx not in st.session_state.extra_temporanei:
                st.session_state.extra_temporanei[idx] = []
                
            st.markdown("Pasto Extra")
            search_input = st.text_input("Cerca alimento extra:", key=f"search_{idx}")
            
            if search_input:
                suggerimenti = [chiave for chiave in DATABASE_EXTRA_UNIFICATO.keys() if search_input.lower() in chiave.lower()]
                if suggerimenti:
                    scelta_cibo = st.selectbox("Seleziona l'alimento corretto:", suggerimenti, key=f"select_cibo_{idx}")
                    if st.button("Aggiungi al Pasto", key=f"add_btn_{idx}", use_container_width=True):
                        dati_cibo = DATABASE_EXTRA_UNIFICATO[scelta_cibo]
                        st.session_state.extra_temporanei[idx].append({"alimento": scelta_cibo, "Kcal": dati_cibo["Kcal"], "info": dati_cibo["info"]})
                        st.rerun()
            
            if st.session_state.extra_temporanei[idx]:
                for item in st.session_state.extra_temporanei[idx]:
                    st.write(f"• {item['alimento']} ({item['info']}) -> {item['Kcal']} Kcal")
                
                if st.button("Concludi Pasto ed Aggiorna", key=f"concludi_{idx}", use_container_width=True, type="secondary"):
                    st.session_state.pasti_generati[idx] = [{"alimento": x["alimento"], "grammi": x["info"], "macro": f"{x['Kcal']} Kcal", "kcal": x["Kcal"]} for x in st.session_state.extra_temporanei[idx]]
                    
                    totale_tutti_i_pasti = 0.0
                    for p_id in range(1, numero_pasti_main + 1):
                        if p_id in st.session_state.pasti_generati:
                            totale_tutti_i_pasti += sum(ing.get("kcal", 0.0) for ing in st.session_state.pasti_generati[p_id])
                    
                    if giorno_workout:
                        st.session_state.cal_generate_wo = totale_tutti_i_pasti
                    else:
                        st.session_state.cal_generate_rest = totale_tutti_i_pasti
                    salva_cache()
                    st.rerun()
        else:
            if idx in st.session_state.pasti_generati and not any("Kcal" in ing["macro"] for ing in st.session_state.pasti_generati[idx]):
                for ingrediente in st.session_state.pasti_generati[idx]:
                    if ingrediente['grammi'] > 0:
                        st.write(f"• **{ingrediente['alimento']}**: {ingrediente['grammi']}g ({ingrediente['macro']})")
            elif idx in st.session_state.pasti_generati:
                for ingrediente in st.session_state.pasti_generati[idx]:
                    st.write(f"• **{ingrediente['alimento']}** ({ingrediente['grammi']}) -> {ingrediente['macro']}")
            else:
                st.info("Pasto non ancora generato.")
            
            # Stampa permanente integratori
            if idx in st.session_state.piani_integratori and st.session_state.piani_integratori[idx]:
                st.markdown("Integratori da assumere:")
                for integratore in st.session_state.piani_integratori[idx]:
                    st.write(f"  - {integratore}")
                
            with col_pasto_dx:
                if st.button("Genera solo questo", key=f"regen_{idx}", use_container_width=True):
                    if riferimento == "Workout":
                        target = {"P": 50, "C": 70, "G": 5}
                    elif riferimento == "Rest":
                        target = {"P": 40, "C": 30, "G": 15}
                    else:
                        target = macro_selezionati_sistema.get(idx, {"P": 40, "C": 50, "G": 10})
                        
                    pasto_singolo, kcal_pasto = genera_singolo_pasto_intelligente(target["P"], target["C"], target["G"], idx)
                    st.session_state.pasti_generati[idx] = pasto_singolo
                    
                    totale_tutti_i_pasti = 0.0
                    for p_id in range(1, numero_pasti_main + 1):
                        if p_id in st.session_state.pasti_generati:
                            totale_tutti_i_pasti += sum(ing.get("kcal", 0.0) for ing in st.session_state.pasti_generati[p_id])
                    
                    if giorno_workout:
                        st.session_state.cal_generate_wo = totale_tutti_i_pasti
                    else:
                        st.session_state.cal_generate_rest = totale_tutti_i_pasti
                    salva_cache()
                    st.rerun()
                    
    st.write("---")
