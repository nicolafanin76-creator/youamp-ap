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

    // Trasforma l'icona della sidebar in un ingranaggio (⚙️)
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
    /* Centraggio globale degli elementi di Streamlit */
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
</style>
"""
components.html(pwa_html, height=0, width=0)

# BANCA DATI UFFICIALE DI YOUAMP COMPLETAMENTE REVISIONATA
BANCA_DATI = {
    # --- CARBOIDRATI ---
    "Riso Basmati": {"P": 8.0, "C": 78.0, "G": 0.8, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Riso Integrale": {"P": 7.5, "C": 73.0, "G": 1.9, "Kcal": 341, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Riso Soffiato": {"P": 7.0, "C": 80.0, "G": 0.5, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Cornflakes": {"P": 7.0, "C": 84.0, "G": 0.8, "Kcal": 370, "cat": "Carboidrati", "sub": "Cereali Colazione"},
    "Granola": {"P": 10.0, "C": 65.0, "G": 12.0, "Kcal": 420, "cat": "Carboidrati", "sub": "Cereali Colazione"},
    "Fiocchi d'Avena": {"P": 11.0, "C": 60.0, "G": 8.0, "Kcal": 366, "cat": "Carboidrati", "sub": "Cereali Colazione"},
    "Pasta di Semola": {"P": 12.5, "C": 71.3, "G": 1.5, "Kcal": 354, "cat": "Carboidrati", "sub": "Pasta"},
    "Pasta Integrale": {"P": 13.0, "C": 65.0, "G": 2.0, "Kcal": 330, "cat": "Carboidrati", "sub": "Pasta"},
    "Pasta di Grano Duro": {"P": 13.0, "C": 73.0, "G": 1.5, "Kcal": 355, "cat": "Carboidrati", "sub": "Pasta"},
    "Cuscus": {"P": 12.8, "C": 72.4, "G": 0.6, "Kcal": 356, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Gallette di Riso": {"P": 7.9, "C": 81.5, "G": 1.1, "Kcal": 371, "cat": "Carboidrati", "sub": "Pane e Sostituti"},
    "Patate": {"P": 2.1, "C": 17.9, "G": 0.1, "Kcal": 80, "cat": "Carboidrati", "sub": "Tuberi"},
    "Patate Dolci": {"P": 1.6, "C": 20.0, "G": 0.1, "Kcal": 86, "cat": "Carboidrati", "sub": "Tuberi"},
    "Rape": {"P": 1.0, "C": 6.0, "G": 0.1, "Kcal": 28, "cat": "Carboidrati", "sub": "Tuberi"},

    # --- PROTEINE ---
    "Petto di Pollo": {"P": 23.0, "C": 0.0, "G": 0.8, "Kcal": 100, "cat": "Proteine", "sub": "Carne Bianca"},
    "Fesa di Tacchino": {"P": 24.0, "C": 0.0, "G": 1.2, "Kcal": 107, "cat": "Proteine", "sub": "Carne Bianca"},
    "Macinato di Pollo": {"P": 21.0, "C": 0.0, "G": 3.0, "Kcal": 111, "cat": "Proteine", "sub": "Carne Bianca"},
    "Coniglio": {"P": 22.0, "C": 0.0, "G": 5.0, "Kcal": 133, "cat": "Proteine", "sub": "Carne Bianca"},
    "Macinato di Coniglio": {"P": 22.0, "C": 0.0, "G": 4.5, "Kcal": 128, "cat": "Proteine", "sub": "Carne Bianca"},
    "Lonza di Maiale": {"P": 22.0, "C": 0.0, "G": 4.0, "Kcal": 124, "cat": "Proteine", "sub": "Carne Rossa"},
    "Macinato Magro di Manzo": {"P": 21.0, "C": 0.0, "G": 5.0, "Kcal": 129, "cat": "Proteine", "sub": "Carne Rossa"},
    "Filetto di Manzo": {"P": 20.5, "C": 0.0, "G": 3.5, "Kcal": 114, "cat": "Proteine", "sub": "Carne Rossa"},
    "Hamburger di Manzo": {"P": 20.0, "C": 0.0, "G": 6.0, "Kcal": 134, "cat": "Proteine", "sub": "Carne Rossa"},
    "Carne di Cavallo": {"P": 21.5, "C": 0.0, "G": 2.7, "Kcal": 111, "cat": "Proteine", "sub": "Carne Rossa"},
    "Bacon": {"P": 14.0, "C": 1.0, "G": 35.0, "Kcal": 375, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Bresaola": {"P": 32.0, "C": 0.0, "G": 2.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Sfilacci di Manzo": {"P": 31.0, "C": 0.0, "G": 3.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Sfilacci di Cavallo": {"P": 32.0, "C": 0.0, "G": 2.5, "Kcal": 150, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Carne Salada": {"P": 23.0, "C": 0.0, "G": 1.5, "Kcal": 105, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Prosciutto Crudo": {"P": 26.0, "C": 0.0, "G": 10.0, "Kcal": 194, "cat": "Proteine", "sub": "Affettati e Salumi"},
    "Albume d'Uovo": {"P": 11.0, "C": 0.7, "G": 0.2, "Kcal": 52, "cat": "Proteine", "sub": "Uova"},
    "Uovo Intero": {"P": 12.4, "C": 0.0, "G": 8.7, "Kcal": 128, "cat": "Proteine", "sub": "Uova"},
    "Kefir": {"P": 3.4, "C": 4.0, "G": 1.5, "Kcal": 43, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Skyr": {"P": 11.0, "C": 3.5, "G": 0.2, "Kcal": 60, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Yogurt Greco 0%": {"P": 10.3, "C": 3.0, "G": 0.0, "Kcal": 53, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Fiocchi di Latte": {"P": 12.0, "C": 3.0, "G": 4.5, "Kcal": 101, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Mozzarella Light": {"P": 18.0, "C": 1.0, "G": 9.0, "Kcal": 157, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Ricotta Light": {"P": 9.0, "C": 4.0, "G": 5.0, "Kcal": 97, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Feta Greca": {"P": 14.0, "C": 4.0, "G": 21.0, "Kcal": 261, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Parmigiano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Grana Padano": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Crema di Riso": {"P": 7.3, "C": 79.0, "G": 1.0, "Kcal": 354, "cat": "Proteine", "sub": "Latticini e Formaggi"},
    "Branzino": {"P": 18.5, "C": 0.0, "G": 2.5, "Kcal": 99, "cat": "Proteine", "sub": "Pesce"},
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
    "Pandoro": {"Kcal": 410, "fetta 100g"},
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

# --- LOGICA DI INIZIALIZZAZIONE E PERSISTENZA AUTOMATICA DATI (LOGIN/SALVATAGGIO) ---
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = 0.0
if "pasti_generati" not in st.session_state:
    st.session_state.pasti_generati = {}
if "extra_temporanei" not in st.session_state:
    st.session_state.extra_temporanei = {}

# Inizializzazione calorie generate per i due regimi
if "cal_generate_wo" not in st.session_state:
    st.session_state.cal_generate_wo = 0.0
if "cal_generate_rest" not in st.session_state:
    st.session_state.cal_generate_rest = 0.0

# Persistenza della memoria macro avanzati (Separati Workout vs Rest)
if "macro_wo_pasti" not in st.session_state:
    st.session_state.macro_wo_pasti = {i: {"P": 40, "C": 50, "G": 10} for i in range(1, 8)}
if "macro_rest_pasti" not in st.session_state:
    st.session_state.macro_rest_pasti = {i: {"P": 40, "C": 30, "G": 15} for i in range(1, 8)}

# --- INTERFACCIA SINISTRA: SIDEBAR (IMPOSTAZIONI SALVATE) ---
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
        sottotipi = sorted(list(
