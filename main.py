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
    "Sfilacci di Cavallo": {"P": 32.0, "C": 0.0, "G": 2.5, "Kcal": 150, "cat": "Proteine", "sub": "S", "P/C"},
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
    "Pizza Margherita": {"Kcal": 700, "info": "1 Porzione Media"},
    "Pizza Farcita": {"Kcal": 950, "info": "1 Porzione Media"},
    "Pasta alla Carbonara": {"Kcal": 850, "info": "1 Piatto Ristorante"},
    "Pasta al Ragù": {"Kcal": 650, "info": "1 Piatto Ristorante"},
    "Panino Fastfood": {"Kcal": 650, "info": "1 Singolo Hamburger Completo"},
    "Patatine Fritte": {"Kcal": 320, "info": "1 Porzione Media"},
    "Sushi": {"Kcal": 450, "info": "Set Misto Combinato 8 pezzi"},
    "Croissant Farcito": {"Kcal": 360, "info": "1 Pezzo Standard"},
    "Gelato Artigianale": {"Kcal": 250, "info": "1 Coppetta Media"},
    "Tiramisù": {"Kcal": 480, "info": "1 Porzione Standard"},
    "Spritz Aperol": {"Kcal": 140, "info": "1 Bicchiere Standard"},
    "Calice di Vino Rosso": {"Kcal": 100, "info": "1 Calice Standard"}
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
        "macro_rest_pasti": st.session_state.get("macro_rest_pasti", {})
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

cache_iniziale = carica_cache()

# Inizializzazione controllata con ripristino da file esterno
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = cache_iniziale.get("acqua_bevuta", 0.0)
if "pasti_generati" not in st.session_state:
    # Convertiamo le chiavi stringa del JSON in int per uniformità
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

# Codice PWA Nativo + Modifica Icona Sidebar + CSS Antioscillazione Rigido
pwa_html = """
<script>
    const manifest = {
        "name": "YouAmp",
        "short_name": "YouAmp",
        "start_url": window.location.href,
        "display": "standalone",
        "background_color": "#111111",
        "theme_color": "#000000"
    };
    const stringManifest = JSON.stringify(manifest);
    const blob = new Blob([stringManifest], {type: 'application/json'});
    const manifestURL = URL.createObjectURL(blob);
    let relManifest = document.createElement('link');
    relManifest.setAttribute('rel', 'manifest');
    relManifest.setAttribute('href', manifestURL);
    document.head.appendChild(relManifest);

    document.addEventListener("DOMContentLoaded", function() {
        setTimeout(function() {
            const sidebarBtn = window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (sidebarBtn) {
                sidebarBtn.innerHTML = '<span style="font-size: 24px; cursor: pointer;">⚙️</span>';
            }
        }, 1000);
    });
</script>
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
components.html(pwa_html, height=0, width=0)

# --- INTERFACCIA SINISTRA: SIDEBAR ---
st.sidebar.title("Profilo e Impostazioni")

nome_atleta = st.sidebar.text_input("Nome Atleta:", value="Nicola Fanin")
altezza = st.sidebar.number_input("Altezza (cm):", min_value=100, max_value=250, value=190)

st.sidebar.write("---")
st.sidebar.subheader("Fabbisogno e consumo calorico consigliato")

pt_k_wo_val = cache_iniziale.get("pt_kcal_wo", 3346)
sp_wo_val = cache_iniziale.get("spesa_wo", 3500)
pt_k_rst_val = cache_iniziale.get("pt_kcal_rest", 2500)
sp_rst_val = cache_iniziale.get("spesa_rest", 2200)

col_wo1, col_wo2 = st.sidebar.columns(2)
with col_wo1:
    pt_kcal_wo = col_wo1.number_input("Fabbisogno WO (Kcal)", value=pt_k_wo_val, key="pt_kcal_wo")
with col_wo2:
    spesa_prevista_wo = col_wo2.number_input("Consumo Stimato WO (Kcal)", value=sp_wo_val, key="spesa_wo")

col_rst1, col_rst2 = st.sidebar.columns(2)
with col_rst1:
    pt_kcal_rest = col_rst1.number_input("Fabbisogno REST (Kcal)", value=pt_k_rst_val, key="pt_kcal_rest")
with col_rst2:
    spesa_prevista_rest = col_rst2.number_input("Consumo Stimato REST (Kcal)", value=sp_rst_val, key="spesa_rest")

st.sidebar.write("---")
st.sidebar.subheader("Target Idrico Specifico")
target_acqua_manuale = st.sidebar.number_input("Indicazione Acqua (Litri)", value=cache_iniziale.get("target_acqua_manuale", 4.0), key="target_acqua_manuale", step=0.5)

st.sidebar.write("---")
st.sidebar.subheader("Dispensa Alimenti")
categorie_lista = ["Carboidrati", "Proteine", "Grassi", "Verdura", "Frutta", "Dolcificanti"]

for categoria in categorie_lista:
    with st.sidebar.expander(categoria.upper()):
        cibi_in_cat = {k: v for k, v in BANCA_DATI_BASE.items() if v["cat"] == categoria}
        sottotipi = sorted(list(set([v["sub"] for v in cibi_in_cat.values()])))
        for sub in sottotipi:
            st.markdown(f"**-- {sub} --**")
            cibi_in_sub = {k: v for k, v in cibi_in_cat.items() if v["sub"] == sub}
            for cibo in cibi_in_sub.keys():
                # Carichiamo la selezione precedente o prendiamo quella di default
                default_slots = st.session_state.dispensa_slots.get(cibo, BANCA_DATI_BASE[cibo]["slots_default"])
                
                # Selezione multipla per slot pasto: C = Colazione, S = Spuntino, P/C = Pranzo/Cena
                scelte_utente = st.multiselect(
                    f"{cibo}", 
                    options=["C", "S", "P/C"], 
                    default=default_slots, 
                    key=f"slots_{cibo}"
                )
                st.session_state.dispensa_slots[cibo] = scelte_utente

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

# Simulatore di ricezione dati App Salute
st.markdown("<h3>Simulatore Sincronizzazione App Connesse</h3>", unsafe_allow_html=True)
col_sal1, col_sal2 = st.columns(2)
with col_sal1:
    st.session_state.app_salute_wo = st.number_input("Kcal Consumate Rilevate App (Giorno WO)", value=st.session_state.app_salute_wo, step=50.0, on_change=salva_cache)
with col_sal2:
    st.session_state.app_salute_rest = st.number_input("Kcal Consumate Rilevate App (Giorno REST)", value=st.session_state.app_salute_rest, step=50.0, on_change=salva_cache)

# Calcolo matematico del deficit reale
deficit_wo = st.session_state.cal_generate_wo - st.session_state.app_salute_wo
deficit_rest = st.session_state.cal_generate_rest - st.session_state.app_salute_rest

# --- CRUSCOTTO ENERGETICO COMPATTO ANTI-OSCILLAZIONE ---
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
        table-layout: fixed; /* Impedisce qualsiasi oscillazione dello schermo */
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

# --- ALGORITMO DI ESTRAZIONE CON FILTRO A MATRICE DI SELEZIONE MULTIPLA ---
def genera_singolo_pasto_intelligente(target_p, target_c, target_g, pasto_id):
    # Mapping logico degli slot
    if pasto_id == 1:
        tag_cercato = "C"
    elif pasto_id in [2, 4, 6, 7]:
        tag_cercato = "S"
    else:
        tag_cercato = "P/C"

    # Filtro della dispensa basato sulla selezione multipla impostata dall'utente nella barra laterale
    carb_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Carboidrati" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    prot_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Proteine" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    grassi_selezionati = [k for k, v in BANCA_DATI_BASE.items() if v["cat"] == "Grassi" and tag_cercato in st.session_state.dispensa_slots.get(k, [])]
    
    # Fallback di emergenza se la dispensa è stata svuotata per quello slot specifico
    fonte_c = random.choice(carb_selezionati) if carb_selezionati else "Gallette di Riso"
    fonte_p = random.choice(prot_selezionati) if prot_selezionati else "Yogurt Greco 0%"
    fonte_g = random.choice(grassi_selezionati) if grassi_selezionati else "Olio Extra Vergine d'Oliva"

    # Bilanciamento ad aggancio incrociato dei macro primari e ombra secondari
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

# Rendering e Gestione dei pasti dinamici
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
