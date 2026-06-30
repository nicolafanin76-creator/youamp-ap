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

# BANCA DATI UFFICIALE DI YOUAMP COMPLETAMENTE AGGIORNATA
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
    "Crema di Mandorle": {"P": 21.0, "C": 19.0, "G": 55.0, "Kcal": 614, "cat": "Grassi", "sub": "Burri e Creme"},
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

# BANCA DATI EXTRA COMPLETA AGGIORNATA SECONDO LE DIRETTIVE EDITORIALI
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
    "Capasanta Gratinata": {"Kcal": 180, "2 Pezzi"},

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
        default_ing = ing in ["Creatina", "Olio di pesce capsule"]
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
st.markdown("<h1 style='text-align: center;'>YouAmp</h1>", unsafe_allow_html=True)
st.write("---")

# Selettore Regime Giornaliero principale centrale
col_toggle = st.columns([1, 2, 1])
with col_toggle[1]:
    giorno_workout = st.toggle("Seleziona Regime Giornaliero", value=True)

if giorno_workout:
    regime_testo = "WORKOUT"
    macro_selezionati_sistema = st.session_state.macro_wo_pasti
    # Calcolo dinamico del deficit per riga workout
    deficit_wo = pt_kcal_wo - st.session_state.cal_generate_wo
    deficit_rest = pt_kcal_rest - st.session_state.cal_generate_rest  # resta statico/precedente
else:
    regime_testo = "REST"
    macro_selezionati_sistema = st.session_state.macro_rest_pasti
    # Calcolo dinamico del deficit per riga rest
    deficit_wo = pt_kcal_wo - st.session_state.cal_generate_wo  # resta statico/precedente
    deficit_rest = pt_kcal_rest - st.session_state.cal_generate_rest

# Scritta monumentale centrata del giorno attivo
st.markdown(f"<h2 style='text-align: center; letter-spacing: 2px; color: #00D26A;'>{regime_testo}</h2>", unsafe_allow_html=True)

# --- CRUSCOTTO MATEMATICO INTERATTIVO A 4 COLONNE ---
st.markdown("<h3 style='text-align: center;'>Quadro Energetico Generale</h3>", unsafe_allow_html=True)

# Intestazione Colonne
c_head1, c_head2, c_head3, c_head4 = st.columns(4)
c_head1.markdown("**Fabbisogno**")
c_head2.markdown("**Consumo Stimato**")
c_head3.markdown("**Calorie Pasti**")
c_head4.markdown("**Deficit**")

# Riga 1: Giorno Workout
c_w1, c_w2, c_w3, c_w4 = st.columns(4)
c_w1.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if giorno_workout else '#222'}; border-radius:5px;'>WO: {pt_kcal_wo} Kcal</div>", unsafe_allow_html=True)
c_w2.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if giorno_workout else '#222'}; border-radius:5px;'>{spesa_prevista_wo} Kcal</div>", unsafe_allow_html=True)
c_w3.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if giorno_workout else '#222'}; border-radius:5px;'>{round(st.session_state.cal_generate_wo)} Kcal</div>", unsafe_allow_html=True)
c_w4.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if giorno_workout else '#222'}; border-radius:5px;'>{round(deficit_wo)} Kcal</div>", unsafe_allow_html=True)

# Riga 2: Giorno Rest
c_r1, c_r2, c_r3, c_r4 = st.columns(4)
c_r1.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if not giorno_workout else '#222'}; border-radius:5px;'>REST: {pt_kcal_rest} Kcal</div>", unsafe_allow_html=True)
c_r2.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if not giorno_workout else '#222'}; border-radius:5px;'>{spesa_prevista_rest} Kcal</div>", unsafe_allow_html=True)
c_r3.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if not giorno_workout else '#222'}; border-radius:5px;'>{round(st.session_state.cal_generate_rest)} Kcal</div>", unsafe_allow_html=True)
c_r4.markdown(f"<div style='padding:8px; background-color:{'#1E3A1E' if not giorno_workout else '#222'}; border-radius:5px;'>{round(deficit_rest)} Kcal</div>", unsafe_allow_html=True)

st.write("---")

# Inserimento Dati Giornalieri Manuali
col_input1, col_input2, col_input3 = st.columns(3)
with col_input1:
    peso_corrente = st.number_input("Peso di Oggi (Kg)", value=91.6, step=0.1)
    ore_sonno = st.number_input("Ore di Somno", value=8.0, step=0.5)
with col_input2:
    passi = st.number_input("Passi Effettuati", value=10000)
    km_percorsi = st.number_input("Distanza (Km)", value=7.2, step=0.1)
with col_input3:
    fc_media = st.number_input("Frequenza Cardiaca (BPM)", value=68)

st.write("---")

# Monitoraggio Idratazione Dinamica Centrata
st.markdown("<h3 style='text-align: center;'>Monitoraggio Idratazione</h3>", unsafe_allow_html=True)
if st.session_state.acqua_bevuta < target_acqua_manuale:
    st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>Bevuti: {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L ❌</h3>", unsafe_allow_html=True)
else:
    st.markdown(f"<h3 style='text-align: center; color: #00D26A;'>Target Raggiunto! {st.session_state.acqua_bevuta:.2f} / {target_acqua_manuale:.2f} L ✓</h3>", unsafe_allow_html=True)

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

# Sezione Fisico
st.markdown("<h3 style='text-align: center;'>Composizione Corporea</h3>", unsafe_allow_html=True)
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

# --- FUNZIONE LOGICA GENERATORE PASTI STANDARD ---
def genera_singolo_pasto(target_p, target_c, target_g):
    carb_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Carboidrati" and dispensa_attiva.get(k, True)]
    prot_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Proteine" and dispensa_attiva.get(k, True)]
    grassi_selezionati = [k for k, v in BANCA_DATI.items() if v["cat"] == "Grassi" and dispensa_attiva.get(k, True)]
    
    fonte_c = random.choice(carb_selezionati) if carb_selezionati else "Riso Basmati"
    fonte_p = random.choice(prot_selezionati) if prot_selezionati else "Petto di Pollo"
    fonte_g = random.choice(grassi_selezionati) if grassi_selezionati else "Olio Extra Vergine d'Oliva"
    
    gr_c = round((target_c / BANCA_DATI[fonte_c]["C"]) * 100) if BANCA_DATI[fonte_c]["C"] > 0 else 0
    gr_p = round((target_p / BANCA_DATI[fonte_p]["P"]) * 100) if BANCA_DATI[fonte_p]["P"] > 0 else 0
    gr_g = round((target_g / BANCA_DATI[fonte_g]["G"]) * 100) if BANCA_DATI[fonte_g]["G"] > 0 else 0
    
    kcal_totali_pasto = (target_p * 4) + (target_c * 4) + (target_g * 9)
    
    return [
        {"alimento": fonte_c, "grammi": gr_c, "macro": f"C: {target_c}g", "kcal": gr_c * (BANCA_DATI[fonte_c]["Kcal"]/100)},
        {"alimento": fonte_p, "grammi": gr_p, "macro": f"P: {target_p}g", "kcal": gr_p * (BANCA_DATI[fonte_p]["Kcal"]/100)},
        {"alimento": fonte_g, "grammi": gr_g, "macro": f"G: {target_g}g", "kcal": gr_g * (BANCA_DATI[fonte_g]["Kcal"]/100)}
    ]

st.markdown("<h3 style='text-align: center;'>Pianificazione Alimentare Giornaliera</h3>", unsafe_allow_html=True)

numero_pasti_main = st.slider("Seleziona numero di pasti giornalieri:", min_value=1, max_value=7, value=5, key="pasti_main")

if st.button("Genera Tutti i Pasti", use_container_width=True, type="primary"):
    st.session_state.pasti_generati = {}
    totale_kcal_giornaliero = 0.0
    
    for idx in range(1, numero_pasti_main + 1):
        target = macro_selezionati_sistema.get(idx, {"P": 40, "C": 50, "G": 10})
        pasto_creato = genera_singolo_pasto(target["P"], target["C"], target["G"])
        st.session_state.pasti_generati[idx] = pasto_creato
        totale_kcal_giornaliero += sum(ing["kcal"] for ing in pasto_creato)
    
    if giorno_workout:
        st.session_state.cal_generate_wo = totale_kcal_giornaliero
    else:
        st.session_state.cal_generate_rest = totale_kcal_giornaliero
    st.rerun()

for idx in range(1, numero_pasti_main + 1):
    st.markdown(f"#### Pasto {idx}")
    
    col_pasto_sx, col_pasto_dx = st.columns([2, 1])
    
    with col_pasto_dx:
        riferimento = st.selectbox("Seleziona Tipo", ["Usa Impostazioni", "Workout", "Rest", "Extra"], key=f"ref_{idx}", label_visibility="collapsed")
    
    with col_pasto_sx:
        if riferimento == "Extra":
            if idx not in st.session_state.extra_temporanei:
                st.session_state.extra_temporanei[idx] = []
                
            st.markdown("<span style='color: #FFB300;'>✨ Pasto Extra</span>", unsafe_allow_html=True)
            search_input = st.text_input("🔍 Cerca alimento extra:", key=f"search_{idx}")
            
            if search_input:
                suggerimenti = [chiave for chiave in BANCA_DATI_EXTRA_SORGENTE.keys() if search_input.lower() in chiave.lower() and dispensa_extra_attiva.get(chiave, True)]
                
                if suggerimenti:
                    scelta_cibo = st.selectbox("Seleziona l'alimento corretto:", suggerimenti, key=f"select_cibo_{idx}")
                    
                    col_ex_btn1, col_ex_btn2 = st.columns(2)
                    with col_ex_btn1:
                        if st.button("➕ Aggiungi al Pasto", key=f"add_btn_{idx}", use_container_width=True):
                            dati_cibo = BANCA_DATI_EXTRA_SORGENTE[scelta_cibo]
                            st.session_state.extra_temporanei[idx].append({"alimento": scelta_cibo, "Kcal": dati_cibo["Kcal"], "info": dati_cibo["info"]})
                            st.toast(f"{scelta_cibo} aggiunto!")
                            st.rerun()
                else:
                    st.warning("Nessun alimento attivo trovato nella dispensa extra.")
            
            if st.session_state.extra_temporanei[idx]:
                st.write("**Elementi inseriti in questo pasto:**")
                totale_pasto_extra = 0.0
                for item in st.session_state.extra_temporanei[idx]:
                    st.write(f"• {item['alimento']} ({item['info']}) → **{item['Kcal']} Kcal**")
                    totale_pasto_extra += item["Kcal"]
                
                if st.button("✓ Concludi Pasto ed Aggiorna", key=f"concludi_{idx}", use_container_width=True, type="secondary"):
                    st.session_state.pasti_generati[idx] = [{"alimento": x["alimento"], "grammi": x["info"], "macro": f"{x['Kcal']} Kcal", "kcal": x["Kcal"]} for x in st.session_state.extra_temporanei[idx]]
                    
                    # Ricalcolo totale delle Kcal generate per il giorno attivo
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
                    st.write(f"• **{ingrediente['alimento']}**: {ingrediente['grammi']}g ({ingrediente['macro']})")
            elif idx in st.session_state.pasti_generati:
                for ingrediente in st.session_state.pasti_generati[idx]:
                    st.write(f"• **{ingrediente['alimento']}** ({ingrediente['grammi']}) → {ingrediente['macro']}")
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
                        
                    pasto_singolo = genera_singolo_pasto(target["P"], target["C"], target["G"])
                    st.session_state.pasti_generati[idx] = pasto_singolo
                    
                    # Ricalcola al volo
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
