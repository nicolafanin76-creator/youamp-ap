import streamlit as st
import random
from datetime import date
import streamlit.components.v1 as components

# Configurazione della pagina stile Mobile/Centrato con il nome ufficiale
st.set_page_config(page_title="YouAmp - Athletic Metrics & Planning", page_icon="⚡", layout="centered")

# Codice PWA Nativo invisibile per installazione su smartphone
pwa_html = """
<script>
    const manifest = {
        "name": "YouAmp Athletic",
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
</script>
"""
components.html(pwa_html, height=0, width=0)

# BANCA DATI COMPLETA DI TUTTI GLI ALIMENTI GENERICI ITALIANI
BANCA_DATI = {
    "Riso Basmati": {"P": 8.0, "C": 78.0, "G": 0.8, "Kcal": 350, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Riso Integrale": {"P": 7.5, "C": 73.0, "G": 1.9, "Kcal": 341, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Pasta di Semola": {"P": 12.5, "C": 71.3, "G": 1.5, "Kcal": 354, "cat": "Carboidrati", "sub": "Pasta"},
    "Pasta Integrale": {"P": 13.0, "C": 65.0, "G": 2.0, "Kcal": 330, "cat": "Carboidrati", "sub": "Pasta"},
    "Cuscus": {"P": 12.8, "C": 72.4, "G": 0.6, "Kcal": 356, "cat": "Carboidrati", "sub": "Riso e Cereali"},
    "Crema di Riso (Polvere)": {"P": 7.3, "C": 79.0, "G": 1.0, "Kcal": 354, "cat": "Carboidrati", "sub": "Cereali Colazione"},
    "Fiocchi d'Avena": {"P": 11.0, "C": 60.0, "G": 8.0, "Kcal": 366, "cat": "Carboidrati", "sub": "Cereali Colazione"},
    "Pane Integrale": {"P": 8.5, "C": 41.0, "G": 4.5, "Kcal": 249, "cat": "Carboidrati", "sub": "Pane e Sostituti"},
    "Gallette di Riso": {"P": 7.9, "C": 81.5, "G": 1.1, "Kcal": 371, "cat": "Carboidrati", "sub": "Pane e Sostituti"},
    "Patate": {"P": 2.1, "C": 17.9, "G": 0.1, "Kcal": 80, "cat": "Carboidrati", "sub": "Tuberi"},
    "Ceci Secchi / Lessati": {"P": 19.0, "C": 47.0, "G": 6.0, "Kcal": 316, "cat": "Carboidrati", "sub": "Legumi"},
    "Piselli": {"P": 5.5, "C": 12.5, "G": 0.6, "Kcal": 76, "cat": "Carboidrati", "sub": "Legumi"},
    "Fagioli Lessati": {"P": 6.0, "C": 16.0, "G": 0.5, "Kcal": 91, "cat": "Carboidrati", "sub": "Legumi"},
    "Miele": {"P": 0.6, "C": 80.0, "G": 0.0, "Kcal": 322, "cat": "Carboidrati", "sub": "Zuccheri e Salse"},
    "Marmellata Senza Zucchero": {"P": 0.5, "C": 25.0, "G": 0.1, "Kcal": 105, "cat": "Carboidrati", "sub": "Zuccheri e Salse"},
    "Petto di Pollo": {"P": 23.0, "C": 0.0, "G": 0.8, "Kcal": 100, "cat": "Proteine", "sub": "Carne Bianca"},
    "Fesa di Tacchino": {"P": 24.0, "C": 0.0, "G": 1.2, "Kcal": 107, "cat": "Proteine", "sub": "Carne Bianca"},
    "Lonza di Maiale Sgrassata": {"P": 22.2, "C": 0.0, "G": 4.2, "Kcal": 127, "cat": "Proteine", "sub": "Carne Rossa"},
    "Filetto di Manzo": {"P": 20.5, "C": 0.0, "G": 3.5, "Kcal": 114, "cat": "Proteine", "sub": "Carne Rossa"},
    "Merluzzo / Nasello": {"P": 17.0, "C": 0.0, "G": 0.3, "Kcal": 71, "cat": "Proteine", "sub": "Pesce Bianco"},
    "Orata": {"P": 19.8, "C": 0.0, "G": 3.7, "Kcal": 113, "cat": "Proteine", "sub": "Pesce Bianco"},
    "Branzino / Spigola": {"P": 18.5, "C": 0.0, "G": 2.5, "Kcal": 99, "cat": "Proteine", "sub": "Pesce Bianco"},
    "Trota": {"P": 19.1, "C": 0.0, "G": 4.3, "Kcal": 115, "cat": "Proteine", "sub": "Pesce Bianco"},
    "Salmone": {"P": 20.0, "C": 0.0, "G": 13.0, "Kcal": 197, "cat": "Proteine", "sub": "Pesce Grasso"},
    "Mazzancolle / Gamberetti": {"P": 18.5, "C": 0.5, "G": 0.6, "Kcal": 81, "cat": "Proteine", "sub": "Crostacei"},
    "Tonno al Naturale": {"P": 25.0, "C": 0.0, "G": 0.5, "Kcal": 104, "cat": "Proteine", "sub": "Pesce in Scatola"},
    "Bresaola": {"P": 32.0, "C": 0.0, "G": 2.0, "Kcal": 151, "cat": "Proteine", "sub": "Affettati Fit"},
    "Affettato di Pollo / Tacchino": {"P": 21.0, "C": 1.0, "G": 1.5, "Kcal": 102, "cat": "Proteine", "sub": "Affettati Fit"},
    "Albume d'Uovo": {"P": 11.0, "C": 0.7, "G": 0.2, "Kcal": 52, "cat": "Proteine", "sub": "Uova"},
    "Uovo Intero": {"P": 12.4, "C": 0.0, "G": 8.7, "Kcal": 128, "cat": "Proteine", "sub": "Uova"},
    "Skyr Naturale": {"P": 11.0, "C": 3.5, "G": 0.2, "Kcal": 60, "cat": "Proteine", "sub": "Latticini Fit"},
    "Kefir Bianco Naturale": {"P": 3.4, "C": 4.0, "G": 1.5, "Kcal": 43, "cat": "Proteine", "sub": "Latticini Fit"},
    "Yogurt Greco 0%": {"P": 10.3, "C": 3.0, "G": 0.0, "Kcal": 53, "cat": "Proteine", "sub": "Latticini Fit"},
    "Stracchino Light": {"P": 15.0, "C": 1.5, "G": 14.0, "Kcal": 192, "cat": "Proteine", "sub": "Formaggi"},
    "Parmigiano / Grana": {"P": 33.0, "C": 0.0, "G": 28.0, "Kcal": 392, "cat": "Proteine", "sub": "Formaggi"},
    "Hummus di Ceci": {"P": 5.0, "C": 14.0, "G": 9.0, "Kcal": 166, "cat": "Proteine", "sub": "Alternative Veg"},
    "Olio Extra Vergine d'Oliva": {"P": 0.0, "C": 0.0, "G": 99.0, "Kcal": 899, "cat": "Grassi", "sub": "Condimenti"},
    "Mandorle": {"P": 22.0, "C": 4.6, "G": 50.0, "Kcal": 579, "cat": "Grassi", "sub": "Frutta Secca"},
    "Noci": {"P": 16.0, "C": 5.5, "G": 65.0, "Kcal": 654, "cat": "Grassi", "sub": "Frutta Secca"},
    "Avocado": {"P": 1.9, "C": 8.6, "G": 15.4, "Kcal": 160, "cat": "Grassi", "sub": "Grassi Vegetali"},
    "Zucchine": {"P": 1.3, "C": 1.4, "G": 0.1, "Kcal": 11, "cat": "Verdura", "sub": "Ortaggi"},
    "Spinaci": {"P": 3.4, "C": 0.6, "G": 0.7, "Kcal": 23, "cat": "Verdura", "sub": "Ortaggi"},
    "Asparagi": {"P": 2.2, "C": 2.1, "G": 0.2, "Kcal": 20, "cat": "Verdura", "sub": "Ortaggi"},
    "Broccoli": {"P": 2.8, "C": 7.0, "G": 0.4, "Kcal": 34, "cat": "Verdura", "sub": "Ortaggi"},
    "Pomodorini": {"P": 1.0, "C": 3.5, "G": 0.2, "Kcal": 18, "cat": "Verdura", "sub": "Ortaggi"},
    "Peperoni": {"P": 0.9, "C": 4.2, "G": 0.3, "Kcal": 22, "cat": "Verdura", "sub": "Ortaggi"},
    "Melanzane": {"P": 1.1, "C": 2.6, "G": 0.1, "Kcal": 15, "cat": "Verdura", "sub": "Ortaggi"},
    "Carote": {"P": 1.1, "C": 7.6, "G": 0.2, "Kcal": 35, "cat": "Verdura", "sub": "Ortaggi"},
    "Cavolo Cappuccio": {"P": 1.4, "C": 4.3, "G": 0.2, "Kcal": 25, "cat": "Verdura", "sub": "Ortaggi"},
    "Succo di Limone": {"P": 0.4, "C": 1.4, "G": 0.0, "Kcal": 6, "cat": "Verdura", "sub": "Condimenti Liquidi"},
    "Melone": {"P": 0.8, "C": 7.4, "G": 0.2, "Kcal": 34, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Cocomero": {"P": 0.6, "C": 3.7, "G": 0.2, "Kcal": 16, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Pesca": {"P": 0.8, "C": 9.1, "G": 0.1, "Kcal": 39, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Uva": {"P": 0.7, "C": 15.6, "G": 0.1, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Mela": {"P": 0.3, "C": 14.0, "G": 0.2, "Kcal": 52, "cat": "Frutta", "sub": "Frutta Standard"},
    "Banana": {"P": 1.1, "C": 23.0, "G": 0.3, "Kcal": 89, "cat": "Frutta", "sub": "Frutta Standard"},
    "Limone": {"P": 0.6, "C": 2.3, "G": 0.0, "Kcal": 11, "cat": "Frutta", "sub": "Frutta Standard"}
}

# --- INTERFACCIA SINISTRA: SIDEBAR ---
st.sidebar.title("👤 Profilo & Impostazioni PT")

nome_atleta = st.sidebar.text_input("Nome Atleta:", value="Nicola Fanin")
altezza = st.sidebar.number_input("Altezza (cm):", min_value=100, max_value=250, value=190)
data_nascita = st.sidebar.date_input("Data di Nascita:", value=date(2000, 1, 1))

st.sidebar.write("---")
st.sidebar.subheader("📋 Direttive Personal Trainer")

# Configurazione Fabbisogni e Consumi affiancati
st.sidebar.markdown("**🏋️ Giorno WORKOUT**")
col_wo1, col_wo2 = st.sidebar.columns(2)
with col_wo1:
    pt_kcal_wo = col_wo1.number_input("Fabbisogno (Kcal)", value=3346, key="pt_kcal_wo")
with col_wo2:
    spesa_prevista_wo = col_wo2.number_input("Consumo Stimato (Kcal)", value=3500, key="spesa_wo")

st.sidebar.markdown("**🍏 Giorno REST**")
col_rst1, col_rst2 = st.sidebar.columns(2)
with col_rst1:
    pt_kcal_rest = col_rst1.number_input("Fabbisogno (Kcal)", value=2500, key="pt_kcal_rest")
with col_rst2:
    spesa_prevista_rest = col_rst2.number_input("Consumo Stimato (Kcal)", value=2200, key="spesa_rest")

st.sidebar.write("---")
st.sidebar.subheader("💧 Target Idrico Specifico")
target_acqua_manuale = st.sidebar.number_input("Indicazione Acqua PT (Litri)", value=4.0, step=0.5)

st.sidebar.write("---")
st.sidebar.subheader("🛒 La Mia Dispensa")
dispensa_attiva = {}
categorie_lista = ["Carboidrati", "Proteine", "Grassi", "Verdura", "Frutta"]

for categoria in categorie_lista:
    with st.sidebar.expander(f"📂 {categoria.upper()}"):
        cibi_in_cat = {k: v for k, v in BANCA_DATI.items() if v["cat"] == categoria}
        sottotipi = sorted(list(set([v["sub"] for v in cibi_in_cat.values()])))
        for sub in sottotipi:
            st.markdown(f"**`-- {sub} --`**")
            cibi_in_sub = {k: v for k, v in cibi_in_cat.items() if v["sub"] == sub}
            for cibo in cibi_in_sub.keys():
                default_val = cibo in ["Riso Basmati", "Petto di Pollo", "Albume d'Uovo", "Olio Extra Vergine d'Oliva", "Zucchine", "Mela"]
                dispensa_attiva[cibo] = st.checkbox(cibo, value=default_val, key=f"disp_{cibo}")

st.sidebar.write("---")
st.sidebar.subheader("💊 Dispensa degli Integratori")
lista_integratori = [
    "Proteine ISO", "Proteine Whey", "Creatina", "Carnitina", "Zinco", 
    "Magnesio", "Cromo", "Vitamina D", "Vitamina C", "Vitamina B", 
    "Berberina", "Olio di pesce capsule", "Elettroliti per acqua", 
    "Potassio", "Aminoacidi essenziali", "Aminoacidi ramificati"
]
integratori_attivi = {}
with st.sidebar.expander("📂 INTEGRATORI DISPONIBILI"):
    for ing in lista_integratori:
        default_ing = ing in ["Creatina", "Olio di pesce capsule"]
        integratori_attivi[ing] = st.checkbox(ing, value=default_ing, key=f"ing_{ing}")

st.sidebar.write("---")
st.sidebar.subheader("⚙️ Configurazione Avanzata Macro Pasti")
numero_pasti = st.sidebar.slider("Seleziona numero di pasti:", min_value=1, max_value=7, value=5)

macro_pasti_personalizzati = {}
for i in range(1, numero_pasti + 1):
    with st.sidebar.expander(f"🍽️ Imposta Macro Pasto {i}"):
        st.markdown(f"**Pasto {i}**")
        p_pasto = st.number_input(f"Proteine (g) - P{i}", value=40, key=f"p_p_{i}")
        c_pasto = st.number_input(f"Carboidrati (g) - P{i}", value=50, key=f"c_p_{i}")
        g_pasto = st.number_input(f"Grassi (g) - P{i}", value=10, key=f"g_p_{i}")
        macro_pasti_personalizzati[i] = {"P": p_pasto, "C": c_pasto, "G": g_pasto}


# --- SCHERMATA PRINCIPALE (TEMPORANEA PER TESTARE LA SIDEBAR) ---
st.title("YouAmp")
st.info("I punti 1, 2 e 3 della Sidebar sono completati con successo! Controlla il menù laterale a sinistra sul tuo telefono o PC.")
st.write("Puoi vedere le nuove sezioni: Direttive PT affiancate, l'indicazione dell'acqua, la nuova dispensa integratori e i configuratori da 1 a 7 pasti per i macro personalizzati.")
