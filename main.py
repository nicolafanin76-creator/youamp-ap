import streamlit as st
import random
from datetime import date
import streamlit.components.v1 as components

# Configurazione della pagina stile Mobile/Centrato con il nome ufficiale
st.set_page_config(page_title="YouAmp", layout="centered")

# Codice PWA Nativo + Modifica Icona Sidebar in Ingranaggio (⚙️)
pwa_html = """
<script>
    const manifest = {
        "name": "YouAmp",
        "short_name": "YouAmp",
        "start_url": window.location.href,
        "display": "standalone",
        "background_color": "#111111",
        "theme_color": "#000000",
        "icons": [{
            "src": "https://cdn-icons-png.flaticon.com/512/8153/8153249.png",
            "sizes": "512x512",
            "type": "image/png"
        }]
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
    }
</style>
"""
components.html(pwa_html, height=0, width=0)

# BANCA DATI METICOLOSA - STRUTTURATA CON SLOT DI CONSUMO ED ESCLUSIONE ERRORI CROSS-MACRO
BANCA_DATI = {
    # --- CARBOIDRATI ---
    "Riso Basmati": {"P": 8.0, "C": 78.0, "G": 0.8, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali", "slot": ["pranzo_cena"]},
    "Riso Integrale": {"P": 7.5, "C": 73.0, "G": 1.9, "Kcal": 341, "cat": "Carboidrati", "sub": "Riso e Cereali", "slot": ["pranzo_cena"]},
    "Riso Soffiato": {"P": 7.0, "C": 80.0, "G": 0.5, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali", "slot": ["colazione", "spuntino"]},
    "Cornflakes": {"P": 7.0, "C": 84.0, "G": 0.8, "Kcal": 370, "cat": "Carboidrati", "sub": "Cereali Colazione", "slot": ["colazione"]},
    "Granola": {"P": 10.0, "C": 65.0, "G": 12.0, "Kcal": 420, "cat": "Carboidrati", "sub": "Cereali Colazione", "slot": ["colazione"]},
    "Fiocchi d'Avena": {"P": 11.0, "C": 60.0, "G": 8.0, "Kcal": 366, "cat": "Carboidrati", "sub": "Cereali Colazione", "slot": ["colazione"]},
    "Pasta di Semola": {"P": 12.5, "C": 71.3, "G": 1.5, "Kcal": 354, "cat": "Carboidrati", "sub": "Pasta", "slot": ["pranzo_cena"]},
    "Pasta Integrale": {"P": 13.0, "C": 65.0, "G": 2.0, "Kcal": 330, "cat": "Carboidrati", "sub": "Pasta", "slot": ["pranzo_cena"]},
    "Pasta di Grano Duro": {"P": 13.0, "C": 73.0, "G": 1.5, "Kcal": 355, "cat": "Carboidrati", "sub": "Pasta", "slot": ["pranzo_cena"]},
    "Cuscus": {"P": 12.8, "C": 72.4, "G": 0.6, "Kcal": 356, "cat": "Carboidrati", "sub": "Riso e Cereali", "slot": ["pranzo_cena"]},
    "Gallette di Riso": {"P": 7.9, "C": 81.5, "G": 1.1, "Kcal": 371, "cat": "Carboidrati", "sub": "Pane e Sostituti", "slot": ["spuntino", "colazione", "pranzo_cena"]},
    "Patate": {"P": 2.1, "C": 17.9, "G": 0.1, "Kcal": 80, "cat": "Carboidrati", "sub": "Tuberi", "slot": ["pranzo_cena"]},
    "Patate Dolci": {"P": 1.6, "C": 20.0, "G": 0.1, "Kcal": 86, "cat": "Carboidrati", "sub": "Tuberi", "slot": ["pranzo_cena"]},
    "Rape": {"P": 1.0, "C": 6.0, "G": 0.1, "Kcal": 28, "cat": "Carboidrati", "sub": "Tuberi", "slot": ["pranzo_cena"]},

    # --- PROTEINE ---
    "Petto di Pollo": {"P": 23.0, "C": 0.0, "G": 0.8, "Kcal": 100, "cat": "Proteine", "sub": "Carne Bianca", "slot": ["pranzo_cena"]},
    "Fesa di Tacchino": {"P": 24.0, "C": 0.0, "G": 1.2, "Kcal": 107, "cat": "Proteine", "sub": "Carne Bianca", "slot": ["pranzo_cena", "spuntino"]},
    "Macinato di Pollo": {"P": 21.0, "C": 0.0, "G": 3.0, "Kcal": 111, "cat": "Proteine", "sub": "Carne Bianca", "slot": ["pranzo_cena"]},
    "Coniglio": {"P": 22.0, "C": 0.0, "G": 5.0, "Kcal": 133, "cat": "Proteine", "sub": "Carne Bianca", "slot": ["pranzo_cena"]},
    "Macinato di Coniglio": {"P": 22.0, "C": 0.0, "G": 4.5, "Kcal": 128, "cat": "Proteine", "sub": "Carne Bianca", "slot": ["pranzo_cena"]},
    "Lonza di Maiale": {"P": 22.0, "C": 0.0, "G": 4.0, "Kcal": 124, "cat": "Proteine", "sub": "Carne Rossa", "slot": ["pranzo_cena"]},
    "Macinato Magro di Manzo": {"P": 21.0, "C": 0.0, "G": 5.0, "Kcal": 129, "cat": "Proteine", "sub": "Carne Rossa", "slot": ["pranzo_cena"]},
    "Filetto di Manzo": {"P": 20.5, "C": 0.0, "G": 3.5, "Kcal": 114, "cat": "Proteine", "sub": "Carne Rossa", "slot": ["pranzo_cena"]},
    "Hamburger di Manzo": {"P": 20.0, "C": 0.0, "G": 6.0, "Kcal": 134, "cat": "Proteine", "sub": "Carne Rossa", "slot": ["pranzo_cena"]},
    "Carne di Cavallo": {"P": 21.5, "C": 0.0, "G": 2.7, "Kcal": 111, "cat": "Proteine", "sub": "Carne Rossa", "slot": ["pranzo_cena"]},
    "Bacon": {"P": 14.0, "C": 1.0, "G": 35.0, "Kcal": 375, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["pranzo_cena"]},
    "Bresaola": {"P": 32.0, "C": 0.0, "G": 2.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["spuntino", "pranzo_cena"]},
    "Sfilacci di Manzo": {"P": 31.0, "C": 0.0, "G": 3.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["spuntino", "pranzo_cena"]},
    "Sfilacci di Cavallo": {"P": 32.0, "C": 0.0, "G": 2.5, "Kcal": 150, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["spuntino", "pranzo_cena"]},
    "Carne Salada": {"P": 23.0, "C": 0.0, "G": 1.5, "Kcal": 105, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["pranzo_cena"]},
    "Prosciutto Crudo": {"P": 26.0, "C": 0.0, "G": 10.0, "Kcal": 194, "cat": "Proteine", "sub": "Affettati e Salumi", "slot": ["spuntino", "pranzo_cena"]},
    "Albume d'Uovo": {"P": 11.0, "C": 0.7, "G": 0.2, "Kcal": 52, "cat": "Proteine", "sub": "Uova", "slot": ["colazione", "pranzo_cena"]},
    "Uovo Intero": {"P": 12.4, "C": 0.0, "G": 8.7, "Kcal": 128, "cat": "Proteine", "sub": "Uova", "slot": ["colazione", "pranzo_cena"]},
    "Kefir": {"P": 3.4, "C": 4.0, "G": 1.5, "Kcal": 43, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["colazione", "spuntino"]},
    "Skyr": {"P": 11.0, "C": 3.5, "G": 0.2, "Kcal": 60, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["colazione", "spuntino"]},
    "Yogurt Greco 0%": {"P": 10.3, "C": 3.0, "G": 0.0, "Kcal": 53, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["colazione", "spuntino"]},
    "Fiocchi di Latte": {"P": 12.0, "C": 3.0, "G": 4.5, "Kcal": 101, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["spuntino", "pranzo_cena"]},
    "Mozzarella Light": {"P": 18.0, "C": 1.0, "G": 9.0, "Kcal": 157, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["pranzo_cena"]},
    "Ricotta Light": {"P": 9.0, "C": 4.0, "G": 5.0, "Kcal": 97, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["pranzo_cena", "spuntino"]},
    "Feta Greca": {"P": 14.0, "C": 4.0, "G": 21.0, "Kcal": 261, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["pranzo_cena"]},
    "Parmigiano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["pranzo_cena", "spuntino"]},
    "Grana Padano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["pranzo_cena", "spuntino"]},
    "Crema di Riso": {"P": 7.3, "C": 79.0, "G": 1.0, "Kcal": 354, "cat": "Proteine", "sub": "Latticini e Formaggi", "slot": ["colazione"]},
    "Branzino": {"P": 18.5, "C": 0.0, "G": 2.5, "Kcal": 99, "cat": "Proteine", "sub": "Pesce", "slot": "Pesce", "sub": "Pesce"},
    "Orata": {"P": 19.8, "C": 0.0, "G": 3.7, "Kcal": 113, "cat": "Proteine", "sub": "Pesce"},
    "Gamberetti": {"P": 18.5, "C": 0.5, "G": 0.6, "Kcal": 81, "cat": "Proteine", "sub": "Pesce"},
    "Salmone": {"P": 20.0, "C": 0.0, "G": 13.0, "Kcal": 197, "cat": "Proteine", "sub": "Pesce"},
    "Trancio di Tonno": {"P": 23.0, "C": 0.0, "G": 1.0, "Kcal": 101, "cat": "Proteine", "sub": "Pesce"},
    "Trancio di Pesce Spada": {"P": 20.0, "C": 0.0, "G": 4.0, "Kcal": 116, "cat": "Proteine", "sub": "Pesce"},
    "Tonno al Naturale": {"P": 25.0, "C": 0.0, "G": 0.5, "Kcal": 104, "cat": "Proteine", "sub": "Pesce in Scatola"},
    "Sgombro in scatola": {"P": 22.0, "C": 0.0, "G": 12.0, "Kcal": 196, "cat": "Proteine", "sub": "Pesce in Scatola"},

    # --- GRASSI, HUMMUS & AVOCADO ---
    "Olio Extra Vergine d'Oliva": {"P": 0.0, "C": 0.0, "G": 99.0, "Kcal": 899, "cat": "Grassi", "sub": "Condimenti"},
    "Noci": {"P": 16.0, "C": 5.5, "G": 65.0, "Kcal": 654, "cat": "Grassi", "sub": "Frutta Secca"},
    "Mandorle": {"P": 22.0, "C": 4.6, "G": 50.0, "Kcal": 579, "cat": "Grassi", "sub": "Frutta Secca"},
    "Cioccolato Fondente": {"P": 5.0, "C": 50.0, "G": 32.0, "Kcal": 515, "cat": "Grassi", "sub": "Cioccolato e Creme"},
    "Burro d'Arachidi": {"P": 25.0, "C": 20.0, "G": 50.0, "Kcal": 588, "cat": "Grassi", "sub": "Burri e Creme"},
    "Crema di Mandorle": {"P": 21.0, "C": 19.0, "G": 55.0, "Kcal": 614, "cat": "Burri e Creme"},
    "Hummus": {"P": 5.0, "C": 14.0, "G": 9.0, "Kcal": 166, "cat": "Grassi", "sub": "Salse Fit"},
    "Guacamole": {"P": 2.0, "C": 8.0, "G": 15.0, "Kcal": 157, "cat": "Grassi", "sub": "Salse Fit"},
    "Avocado": {"P": 1.9, "C": 8.6, "G": 15.4, "Kcal": 160, "cat": "Grassi", "sub": "Salse Fit"},

    # --- VERDURE & LEGUMI ---
    "Broccoli": {"P": 2.8, "C": 7.0, "G": 0.4, "Kcal": 34, "cat": "Verdura", "sub": "Ortaggi"},
    "Lattuga": {"P": 1.3, "C": 2.2, "G": 0.2, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi"},
    "Rucola": {"P": 2.6, "C": 3.7, "G": 0.7, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi"},
    "Pomodorini": {"P": 1.0, "C": 3.5, "G": 0.2, "Kcal": 18, "cat": "Verdura", "sub": "Ortaggi"},
    "Pomodori": {"P": 0.9, "C": 3.9, "G": 0.2, "Kcal": 18, "cat": "Verdura", "sub": "Ortaggi"},
    "Peperoni": {"P": 0.9, "C": 4.2, "G": 0.3, "Kcal": 22, "cat": "Verdura", "sub": "Ortaggi"},
    "Melanzane": {"P": 1.1, "C": 2.6, "G": 0.1, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi"},
    "Carote": {"P": 1.1, "C": 7.6, "G": 0.2, "Kcal": 35, "cat": "Verdura", "sub": "Ortaggi"},
    "Finocchi": {"P": 1.2, "C": 7.3, "G": 0.2, "Kcal": 31, "cat": "Verdura", "sub": "Ortaggi"},
    "Cavolfiore": {"P": 1.9, "C": 5.0, "G": 0.3, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi"},
    "Cetriolo": {"P": 0.6, "C": 3.6, "G": 0.1, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi"},
    "Cavolo Cappuccio": {"P": 1.4, "C": 4.3, "G": 0.2, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi"},
    "Cicoria": {"P": 1.7, "C": 4.0, "G": 0.3, "Kcal": 23, "cat": "Verdura", "sub": "Ortaggi"},
    "Bieta": {"P": 1.8, "C": 3.7, "G": 0.3, "Kcal": 19, "cat": "Verdura", "sub": "Ortaggi"},
    "Porro": {"P": 1.5, "C": 14.0, "G": 0.3, "Kcal": 61, "cat": "Verdura", "sub": "Ortaggi"},
    "Cipolla": {"P": 1.1, "C": 9.3, "G": 0.1, "Kcal": 40, "cat": "Verdura", "sub": "Ortaggi"},
    "Sedano": {"P": 0.7, "C": 3.0, "G": 0.2, "Kcal": 16, "cat": "Verdura", "sub": "Ortaggi"},
    "Cavolo Nero": {"P": 3.3, "C": 6.0, "G": 0.7, "Kcal": 49, "cat": "Verdura", "sub": "Ortaggi"},
    "Zucca": {"P": 1.0, "C": 6.5, "G": 0.1, "Kcal": 26, "cat": "Verdura", "sub": "Zucca"},
    "Funghi": {"P": 3.1, "C": 3.3, "G": 0.3, "Kcal": 22, "cat": "Verdura", "sub": "Ortaggi"},
    "Zucchine": {"P": 1.3, "C": 1.4, "G": 0.1, "Kcal": 11, "cat": "Verdura", "sub": "Ortaggi"},
    "Spinaci": {"P": 3.4, "C": 0.6, "G": 0.7, "Kcal": 23, "cat": "Verdura", "sub": "Ortaggi"},
    "Fagiolini": {"P": 1.8, "C": 7.0, "G": 0.2, "Kcal": 31, "cat": "Verdura", "sub": "Ortaggi"},
    "Piselli": {"P": 5.4, "C": 14.5, "G": 0.4, "Kcal": 81, "cat": "Verdura", "sub": "Legumi"},
    "Fagioli": {"P": 21.0, "C": 50.0, "G": 1.2, "Kcal": 291, "cat": "Verdura", "sub": "Legumi"},
    "Lenticchie": {"P": 25.0, "C": 54.0, "G": 1.1, "Kcal": 325, "cat": "Verdura", "sub": "Legumi"},
    "Ceci": {"P": 19.0, "C": 47.0, "G": 6.0, "Kcal": 316, "cat": "Verdura", "sub": "Legumi"},

    # --- FRUTTA ---
    "Banana": {"P": 1.1, "C": 23.0, "G": 0.3, "Kcal": 89, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Kiwi": {"P": 1.1, "C": 15.0, "G": 0.5, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Pesca": {"P": 0.8, "C": 9.1, "G": 0.1, "Kcal": 39, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Fragole": {"P": 0.7, "C": 7.7, "G": 0.3, "Kcal": 32, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Frutti Rossi": {"P": 1.0, "C": 12.0, "G": 0.5, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Melone": {"P": 0.8, "C": 7.4, "G": 0.2, "Kcal": 34, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Anguria": {"P": 0.6, "C": 3.7, "G": 0.2, "Kcal": 16, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Pera": {"P": 0.3, "C": 15.0, "G": 0.1, "Kcal": 57, "cat": "Frutta", "sub": "Frutta Standard"},
    "Uva": {"P": 0.7, "C": 15.6, "G": 0.1, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Standard"},
    "Arancia": {"P": 0.9, "C": 12.0, "G": 0.1, "Kcal": 47, "cat": "Frutta", "sub": "Frutta Standard"},
    "Clementine": {"P": 0.9, "C": 12.0, "G": 0.1, "Kcal": 47, "cat": "Frutta", "sub": "Frutta Standard"},
    "Ananas": {"P": 0.5, "C": 13.0, "G": 0.1, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Esotica"},
    "Mango": {"P": 0.8, "C": 15.0, "G": 0.4, "Kcal": 60, "cat": "Frutta", "sub": "Frutta Esotica"},
    "Cocco": {"P": 3.3, "C": 15.0, "G": 33.0, "Kcal": 354, "cat": "Frutta", "sub": "Frutta Esotica"},
    "Albicocche": {"P": 1.4, "C": 11.0, "G": 0.4, "Kcal": 48, "cat": "Frutta", "sub": "Frutta Standard"},
    "Ciliegie": {"P": 1.0, "C": 16.0, "G": 0.2, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Standard"},
    "Mela": {"P": 0.3, "C": 14.0, "G": 0.2, "Kcal": 52, "cat": "Frutta", "sub": "Frutta Standard"},
    "Macedonia di Frutta": {"P": 0.8, "C": 11.5, "G": 0.2, "Kcal": 50, "cat": "Frutta", "sub": "Frutta Standard"},

    # --- SUCCHI, BEVANDE & BEVANDE ZERO ---
    "Succo d'Arancia": {"P": 0.7, "C": 10.0, "G": 0.2, "Kcal": 45, "cat": "Frutta", "sub": "Succhi e Bevande"},
    "Succhi senza Zucchero": {"P": 0.4, "C": 6.0, "G": 0.1, "Kcal": 28, "cat": "Frutta", "sub": "Succhi e Bevande"},
    "Bibite senza Zucchero": {"P": 0.0, "C": 0.1, "G": 0.0, "Kcal": 1, "cat": "Frutta", "sub": "Succhi e Bevande"},

    # --- DOLCIFICANTI ---
    "Miele": {"P": 0.6, "C": 80.0, "G": 0.0, "Kcal": 322, "cat": "Dolcificanti", "sub": "Zuccheri Fit"},
    "Marmellata senza Zucchero": {"P": 0.5, "C": 25.0, "G": 0.1, "Kcal": 105, "cat": "Dolcificanti", "sub": "Zuccheri Fit"},
    "Stevia": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Dolcificanti", "sub": "Zuccheri Fit"},
    "Dolcificante": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Dolcificanti", "sub": "Zuccheri Fit"}
}

# BANCA DATI EXTRA COMPLETA E RETTIFICATA NELL'ORTOGRAFIA
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
    "Patatine Fritte": {"Kcal": 320, "info": "1 Porzione Media"},

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
for k, v in BANCA_DATI.items():
    DATABASE_EXTRA_UNIFICATO[f"{k} (Porzione da 100g)"] = {"Kcal": v["Kcal"], "info": "100g standard"}

# --- INIZIALIZZAZIONE STATI DI SESSIONE PER PERSISTENZA ---
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = 0.0
if "pasti_generati" not in st.session_state:
    st.session_state.pasti_generati = {}
if "extra_temporanei" not in st.session_state:
    st.session_state.extra_temporanei = {}
if "piani_integratori" not in st.session_state:
    st.session_state.piani_integratori = {}

if "cal_generate_wo" not in st.session_state:
    st.session_state.cal_generate_wo = 0.0
if "cal_generate_rest" not in st.session_state:
    st.session_state.cal_generate_rest = 0.0

# Input reali provenienti dall'App Salute (Dinamici)
if "app_salute_wo" not in st.session_state:
    st.session_state.app_salute_wo = 3500.0
if "app_salute_rest" not in st.session_state:
    st.session_state.app_salute_rest = 2200.0

if "macro_wo_pasti" not in st.session_state:
    st.session_state.macro_wo_pasti = {i: {"P": 40, "C": 50, "G": 10} for i in range(1, 8)}
if "macro_rest_pasti" not in st.session_state:
    st.session_state.macro_rest_pasti = {i: {"P": 40, "C": 30, "G": 15} for i in range(1, 8)}

# --- INTERFACCIA SINISTRA: SIDEBAR ---
st.sidebar.title("Profilo e Impostazioni")

foto_profilo = st.sidebar.file_uploader("Carica la tua foto profilo:", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
if foto_profilo is not None:
    st.sidebar.image(foto_profilo, width=120)

nome_atleta = st.sidebar.text_input("Nome Atleta:", value="Nicola Fanin")
altezza = st.sidebar.number_input("Altezza (cm):", min_value=100, max_value=250, value=190)
data_nascita = st.sidebar.date_input("Data di Nascita:", value=date(2000, 1, 1), min_value=date(1920, 1, 1), max_value=date(2026, 12, 31))
eta = 2026 - data_nascita.year - ((6, 30) < (data_nascita.month, data_nascita.day))

st.sidebar.write("---")
st.sidebar.subheader("Fabbisogno e consumo calorico consigliato")

col_wo1, col_wo2 = st.sidebar.columns(2)
with col_wo1:
    pt_kcal_wo = col_wo1.number_input("Fabbisogno WO (Kcal)", value=3346, key="pt_kcal_wo")
with col_wo2:
    spesa_prevista_wo = col_wo2.number_input("Consumo Stimato WO (Kcal)", value=3500, key="spesa_wo")

col_rst1, col_rst2 = st.sidebar.columns(2)
with col_rst1:
    pt_kcal_rest = col_rst1.number_input("Fabbisogno REST (Kcal)", value=2500, key="pt_kcal_rest")
with col_rst2:
    spesa_prevista_rest = col_rst2.number_input("Consumo Stimato REST (Kcal)", value=2200, key="spesa_rest")

st.sidebar.write("---")
st.sidebar.subheader("Target Idrico Specifico")
target_acqua_manuale = st.sidebar.number_input("Indicazione Acqua (Litri)", value=4.0, step=0.5)

st.sidebar.write("---")
st.sidebar.subheader("Dispensa Alimenti")
dispensa_attiva = {}
categorie_lista = ["Carboidrati", "Proteine", "Grassi", "Verdura", "Frutta", "Dolcificanti"]

for categoria in categorie_lista:
    with st.sidebar.expander(categoria.upper()):
        cibi_in_cat = {k: v for k, v in BANCA_DATI.items() if v["cat"] == categoria}
        sottotipi = sorted(list(set([v["sub"] for v in cibi_in_cat.values()])))
        for sub in sottotipi:
            st.markdown(f"**-- {sub} --**")
            cibi_in_sub = {k: v for k, v in cibi_in_cat.items() if v["sub"] == sub}
            for cibo in cibi_in_sub.keys():
                default_val = cibo in ["Riso Basmati", "Petto di Pollo", "Albume d'Uovo", "Olio Extra Vergine d'Oliva", "Zucchine", "Mela", "Stevia"]
                dispensa_attiva[cibo] = st.checkbox(cibo, value=default_val, key=f"disp_{cibo}")

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
if st.sidebar.button("Salva Impostazioni e Chiudi", use_container_width=True):
    components.html("""<script>window.parent.document.querySelector('.stSidebar [data-testid="collapsedControl"]').click();</script>""", height=0, width=0)


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

# --- SIMULATORE TRASMISSIONE DATI REALI DA APP CONNESSE (SALUTE / ANDROID) ---
st.markdown("<h3>Simulatore Sincronizzazione App Connesse</h3>", unsafe_allow_html=True)
col_sal1, col_sal2 = st.columns(2)
with col_sal1:
    st.session_state.app_salute_wo = st.number_input("Kcal Consumate Rilevate App (Giorno WO)", value=st.session_state.app_salute_wo, step=50.0)
with col_sal2:
    st.session_state.app_salute_rest = st.number_input("Kcal Consumate Rilevate App (Giorno REST)", value=st.session_state.app_salute_rest, step=50.0)

# CALCOLO STRITTISSIMO DEL DEFICIT REALE: ( calorie dei pasti - consumo reale rilevato dall'app )
deficit_wo = st.session_state.cal_generate_wo - st.session_state.app_salute_wo
deficit_rest = st.session_state.cal_generate_rest - st.session_state.app_salute_rest

# --- CRUSCOTTO ENERGETICO COMPATTO AD ALTA VISIBILITÀ ---
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
            <th>Regime</th>
            <th>Fabbisogno PT</th>
            <th>Consumo Stimato PT</th>
            <th>Calorie Pasti</th>
            <th>Consumo Reale App</th>
            <th>Deficit Reale</th>
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

# Sezione Pianificatore Integratori
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
                st.rerun()
    if st.session_state.piani_integratori:
        if st.button("Svuota Piano Integratori Memoria", use_container_width=True, type="secondary"):
            st.session_state.piani_integratori = {}
            st.rerun()
else:
    st.info("Attiva gli integratori nelle impostazioni della barra laterale per associarli.")

st.write("---")

# Inserimento Dati Giornalieri Manuali
col_input1, col_input2, col_input3 = st.columns(3)
with col_input1:
    peso_corrente = st.number_input("Peso di Oggi (Kg)", value=91.6, step=0.1)
    ore_sonno = st.number_input("Ore di Sonno", value=8.0, step=0.5)
with col_input2:
    passi = st.number_input("Passi Effettuati", value=10000)
    km_percorsi = st.number_input("Distanza (Km)", value=7.2, step=0.1)
with col_input3:
    fc_media = st.number_input("Frequenza Cardiaca (BPM)", value=68)

st.write("---")

# Monitoraggio Idratazione
st.markdown("<h3>Monitoraggio Idratazione</h3>", unsafe_allow_html=True)
if st.session_state.acqua_bevuta < target_acqua_manuale:
    st.markdown(f"<h3>Bevuti: {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3>Target Raggiunto! {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L</h3>", unsafe_allow_html=True)

col_w_btn = st.columns([1, 1, 1, 1, 1, 1])
with col_w_btn[1]:
    if st.button("+50ml"): st.session_state.acqua_bevuta += 0.05
with col_w_btn[2]:
    if st.button("+250ml"): st.session_state.acqua_bevuta += 0.25
with col_w_btn[3]:
    if st.button("+500ml"): st.session_state.acqua_bevuta += 0.50
with col_w_btn[4]:
    if st.button("Reset"): st.session_state.acqua_bevuta = 0.0

st.write("---")

# Composizione Corporea
st.markdown("<h3>Composizione Corporea</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Plicometria", "Circonferenze"])

with tab1:
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        st.info("Petto: diagonale\n\nAddome: verticale\n\nCoscia: verticale")
    with col_pl2:
        plica_petto = st.number_input("Plica Petto (mm)", min_value=0.0, value=12.0, step=0.1)
        plica_addome = st.number_input("Plica Addome (mm)", min_value=0.0, value=18.0, step=0.1)
        plica_coscia = st.number_input("Plica Coscia (mm)", min_value=0.0, value=15.0, step=0.1)
    
    somma_pliche = plica_petto + plica_addome + plica_coscia
    if somma_pliche > 0:
        bd = 1.10938 - (0.0008267 * somma_pliche) + (0.0000016 * (somma_pliche ** 2)) - (0.0002574 * eta)
        percentuale_grasso = round(((4.95 / bd) - 4.50) * 100, 1)
        massa_grassa_kg = round((peso_corrente * percentuale_grasso) / 100, 1)
        massa_magra_kg = round(peso_corrente - massa_grassa_kg, 1)
    else:
        percentuale_grasso, massa_grassa_kg, massa_magra_kg = 0.0, 0.0, 0.0
        
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: st.metric(label="Grasso Corporeo", value=f"{percentuale_grasso} %")
    with col_f2: st.metric(label="Massa Grassa", value=f"{massa_grassa_kg} Kg")
    with col_f3: st.metric(label="Massa Magra", value=f"{massa_magra_kg} Kg")

with tab2:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("**Centro Corpo**")
        c_collo = st.number_input("Collo (cm)", value=41.0)
        c_spalle = st.number_input("Spalle (cm)", value=128.0)
        c_petto = st.number_input("Petto (cm)", value=112.0)
        c_vita = st.number_input("Vita (cm)", value=86.0)
        c_fianchi = st.number_input("Fianchi (cm)", value=98.0)
    with col_c2:
        st.markdown("**Simmetria Arti (DX vs SX)**")
        c_bicipite_dx = st.number_input("Bicipite DX (cm)", value=42.0)
        c_bicipite_sx = st.number_input("Bicipite SX (cm)", value=41.5)
        c_avambraccio_dx = st.number_input("Avambraccio DX (cm)", value=34.0)
        c_avambraccio_sx = st.number_input("Avambraccio SX (cm)", value=33.8)
        c_coscia_dx = st.number_input("Coscia DX (cm)", value=62.0)
        c_coscia_sx = st.number_input("Coscia SX (cm)", value=61.2)
        c_polpaccio_dx = st.number_input("Polpaccio DX (cm)", value=40.0)
        c_polpaccio_sx = st.number_input("Polpaccio SX (cm)", value=40.0)

st.write("---")

# --- NUOVO ALGORITMO DI BILANCIAMENTO INCROCIATO DEI MACRO INTER-DIPENDENTI ---
def genera_singolo_pasto_intelligente(target_p, target_c, target_g, pasto_id):
    # Selezione in base alla tipologia cronologica del pasto per dare un senso gastronomico reale
    if pasto_id == 1:
        tag_filtro = "colazione"
    elif pasto_id in [2, 4, 6, 7]:
        tag_filtro = "spuntino"
    else:
        tag_filtro = "pranzo_cena"

    carb_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Carboidrati" and dispensa_attiva.get(k, True) and tag_filtro in v["slot"]]
    prot_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Proteine" and dispensa_attiva.get(k, True) and tag_filtro in v["slot"]]
    grassi_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Grassi" and dispensa_attiva.get(k, True)]
    
    fonte_c = random.choice(carb_selezionati) if carb_selezionati else "Gallette di Riso"
    fonte_p = random.choice(prot_selezionati) if prot_selezionati else "Yogurt Greco 0%"
    fonte_g = random.choice(grassi_selezionati) if grassi_selezionati else "Olio Extra Vergine d'Oliva"

    # Fase 1: Calcolo dei Carboidrati principali
    c_purezza = BANCA_DATI[fonte_c]["C"] / 100.0
    gr_c = round(target_c / c_purezza) if c_purezza > 0 else 0
    
    # Estraiamo i macro ombra dei carboidrati generati
    p_ombra_c = gr_c * (BANCA_DATI[fonte_c]["P"] / 100.0)
    g_ombra_c = gr_c * (BANCA_DATI[fonte_c]["G"] / 100.0)

    # Fase 2: Calcolo delle Proteine, compensando i macro ombra già inseriti dal carboidrato
    target_p_rimanente = max(0.0, target_p - p_ombra_c)
    p_purezza = BANCA_DATI[fonte_p]["P"] / 100.0
    gr_p = round(target_p_rimanente / p_purezza) if p_purezza > 0 else 0

    # Estraiamo i macro ombra del blocco proteico generato (es. i grassi intrinseci della ricotta/feta)
    c_ombra_p = gr_p * (BANCA_DATI[fonte_p]["C"] / 100.0)
    g_ombra_p = gr_p * (BANCA_DATI[fonte_p]["G"] / 100.0)

    # Fase 3: Calcolo dei Grassi (Olio o frutta secca), compensando l'accumulo ombra dei grassi precedenti
    target_g_rimanente = max(0.0, target_g - g_ombra_c - g_ombra_p)
    g_purezza = BANCA_DATI[fonte_g]["G"] / 100.0
    gr_g = round(target_g_rimanente / g_purezza) if g_purezza > 0 else 0

    # Calcolo esatto delle Kcal complessive finali generate dal pasto reale
    kcal_c = gr_c * (BANCA_DATI[fonte_c]["Kcal"] / 100.0)
    kcal_p = gr_p * (BANCA_DATI[fonte_p]["Kcal"] / 100.0)
    kcal_g = gr_g * (BANCA_DATI[fonte_g]["Kcal"] / 100.0)
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
    st.rerun()

# Rendering e Gestione dei pasti
for idx in range(1, numero_pasti_main + 1):
    # Calcolo etichetta del tipo di pasto
    if idx == 1:
        tipo_nome_etichetta = "Colazione"
    elif idx in [2, 4, 6, 7]:
        tipo_nome_etichetta = "Spuntino"
    else:
        tipo_nome_etichetta = "Pranzo/Cena"

    # Recupero e stampa delle Kcal generate per il singolo blocco pasto
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
                    col_ex_btn1, col_ex_btn2 = st.columns(2)
                    with col_ex_btn1:
                        if st.button("Aggiungi al Pasto", key=f"add_btn_{idx}", use_container_width=True):
                            dati_cibo = DATABASE_EXTRA_UNIFICATO[scelta_cibo]
                            st.session_state.extra_temporanei[idx].append({"alimento": scelta_cibo, "Kcal": dati_cibo["Kcal"], "info": dati_cibo["info"]})
                            st.rerun()
                else:
                    st.warning("Nessun alimento trovato.")
            
            if st.session_state.extra_temporanei[idx]:
                st.write("Elementi inseriti in questo pasto:")
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
                    st.rerun()
            else:
                st.info("Digita un alimento sopra per comporre il tuo pasto fuori menù.")
                
        else:
            if idx in st.session_state.pasti_generati and not any("Kcal" in ing["macro"] for ing in st.session_state.pasti_generati[idx]):
                for ingrediente in st.session_state.pasti_generati[idx]:
                    if ingrediente['grammi'] > 0:
                        st.write(f"• **{ingrediente['alimento']}**: {ingrediente['grammi']}g ({ingrediente['macro']})")
                
                # Sostituzione Shaker Proteico
                pasto_ha_cibo_proteico = any(ing["alimento"] in [x for x, y in BANCA_DATI.items() if y["cat"] == "Proteine" and "Polvere" not in x] for ing in st.session_state.pasti_generati[idx])
                if pasto_ha_cibo_proteico:
                    col_pasto_dx_btn = st.columns([1,1])
                    with col_pasto_dx_btn[0]:
                        riferimento_shk = st.selectbox("Cambia in Shake", ["Scegli Integratore", "Proteine ISO", "Proteine Whey"], key=f"shk_ref_{idx}", label_visibility="collapsed")
                    with col_pasto_dx_btn[1]:
                        if st.button("Sostituisci", key=f"swap_shaker_{idx}"):
                            if riferimento_shk != "Scegli Integratore":
                                purezza = 0.90 if riferimento_shk == "Proteine ISO" else 0.80
                                target_p_originale = st.session_state.pasti_generati[idx][0]["target_orig"]
                                grammi_polvere_necessari = round(target_p_originale / purezza)
                                kcal_shaker = target_p_originale * 4
                                
                                for ing in st.session_state.pasti_generati[idx]:
                                    if ing.get("tipo_cat") == "Proteine":
                                        ing["alimento"] = f"{riferimento_shk} in Polvere"
                                        ing["grammi"] = grammi_polvere_necessari
                                        ing["macro"] = f"P: {target_p_originale}g"
                                        ing["kcal"] = kcal_shaker
                                
                                totale_tutti_i_pasti = 0.0
                                for p_id in range(1, numero_pasti_main + 1):
                                    if p_id in st.session_state.pasti_generati:
                                        totale_tutti_i_pasti += sum(ing.get("kcal", 0.0) for ing in st.session_state.pasti_generati[p_id])
                                if giorno_workout:
                                    st.session_state.cal_generate_wo = totale_tutti_i_pasti
                                else:
                                    st.session_state.cal_generate_rest = totale_tutti_i_pasti
                                st.rerun()

            elif idx in st.session_state.pasti_generati:
                for ingrediente in st.session_state.pasti_generati[idx]:
                    st.write(f"• **{ingrediente['alimento']}** ({ingrediente['grammi']}) -> {ingrediente['macro']}")
            else:
                st.info("Pasto non ancora generato.")
            
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
                    st.rerun()
                    
    st.write("---")
