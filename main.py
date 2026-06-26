import streamlit as st
import random
from datetime import date
import streamlit.components.v1 as components

# Configurazione della pagina stile Mobile/Centrato con il nome ufficiale
st.set_page_config(page_title="YouAmp - Athletic Metrics & Planning", page_icon="⚡", layout="centered")

# Codice PWA Nativo invisibile per ingannare iPhone e Android e sbloccare l'installazione a tutto schermo
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

# Inizializzazione dello stato per il contatore dell'acqua
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = 0.0

# Intestazione Ufficiale YouAmp
st.title("⚡ YouAmp — Athletic Metrics & Planning")
st.write("---")

# BANCA DATI COMPLETA DI TUTTI GLI ALIMENTI GENERICI ITALIANI AGGIORNATI
BANCA_DATI = {
    # === 1. CARBOIDRATI ===
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
    
    # === 2. PROTEINE ===
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

    # === 3. GRASSI ===
    "Olio Extra Vergine d'Oliva": {"P": 0.0, "C": 0.0, "G": 99.0, "Kcal": 899, "cat": "Grassi", "sub": "Condimenti"},
    "Mandorle": {"P": 22.0, "C": 4.6, "G": 50.0, "Kcal": 579, "cat": "Grassi", "sub": "Frutta Secca"},
    "Noci": {"P": 16.0, "C": 5.5, "G": 65.0, "Kcal": 654, "cat": "Grassi", "sub": "Frutta Secca"},
    "Avocado": {"P": 1.9, "C": 8.6, "G": 15.4, "Kcal": 160, "cat": "Grassi", "sub": "Grassi Vegetali"},

    # === 4. VERDURA ===
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

    # === 5. FRUTTA ===
    "Melone": {"P": 0.8, "C": 7.4, "G": 0.2, "Kcal": 34, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Cocomero": {"P": 0.6, "C": 3.7, "G": 0.2, "Kcal": 16, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Pesca": {"P": 0.8, "C": 9.1, "G": 0.1, "Kcal": 39, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Uva": {"P": 0.7, "C": 15.6, "G": 0.1, "Kcal": 61, "cat": "Frutta", "sub": "Frutta Dolce"},
    "Mela": {"P": 0.3, "C": 14.0, "G": 0.2, "Kcal": 52, "cat": "Frutta", "sub": "Frutta Standard"},
    "Banana": {"P": 1.1, "C": 23.0, "G": 0.3, "Kcal": 89, "cat": "Frutta", "sub": "Frutta Standard"},
    "Limone": {"P": 0.6, "C": 2.3, "G": 0.0, "Kcal": 11, "cat": "Frutta", "sub": "Frutta Standard"},

    # === 6. INTEGRAZIONE ===
    "Creatina Monoidrato": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Integrazione", "sub": "Performance"},
    "Aminoacidi BCAA 2:1:1": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Integrazione", "sub": "Performance"},
    "Omega 3 (Capsule)": {"P": 0.0, "C": 0.0, "G": 1.0, "Kcal": 9, "cat": "Integrazione", "sub": "Salute"},
    "Multivitaminico Minerale": {"P": 0.0, "C": 0.0, "G": 0.0, "Kcal": 0, "cat": "Integrazione", "sub": "Salute"}
}

# --- SIDEBAR: PROFILO UTENTE ED ETÀ ---
st.sidebar.header("👤 Profilo Utente")
nome_atleta = st.sidebar.text_input("Nome Atleta:", value="Nicola Fanin")
altezza = st.sidebar.number_input("Altezza (cm):", min_value=100, max_value=250, value=190)
data_nascita = st.sidebar.date_input("Data di Nascita:", value=date(2000, 1, 1))
eta = 2026 - data_nascita.year - ((6, 26) < (data_nascita.month, data_nascita.day))

# --- SIDEBAR: INTERFACCIA COMPILAZIONE DISPENSA ---
st.sidebar.write("---")
st.sidebar.header("🛒 La Mia Dispensa")
dispensa_attiva = {}
categorie_lista = ["Carboidrati", "Proteine", "Grassi", "Verdura", "Frutta", "Integrazione"]

for categoria in categorie_lista:
    with st.sidebar.expander(f"📂 {categoria.upper()}"):
        cibi_in_cat = {k: v for k, v in BANCA_DATI.items() if v["cat"] == categoria}
        sottotipi = sorted(list(set([v["sub"] for v in cibi_in_cat.values()])))
        for sub in sottotipi:
            st.markdown(f"**`-- {sub} --`**")
            cibi_in_sub = {k: v for k, v in cibi_in_cat.items() if v["sub"] == sub}
            for cibo in cibi_in_sub.keys():
                default_val = cibo in ["Riso Basmati", "Petto di Pollo", "Albume d'Uovo", "Olio Extra Vergine d'Oliva", "Zucchine", "Mela", "Creatina Monoidrato"]
                dispensa_attiva[cibo] = st.checkbox(cibo, value=default_val, key=f"disp_{cibo}")


# --- SEZIONE 1: CONFIGURATORE DIRETTIVE PT ---
st.subheader("📋 Configurazione Direttive Personal Trainer")
col_pt1, col_pt2 = st.columns(2)
with col_pt1:
    st.markdown("### 🏋️ Giorno WORKOUT")
    pt_kcal_wo = st.number_input("Target Ingestione WO (Kcal)", value=3346)
    pt_p_wo = st.number_input("Proteine WO (g)", value=200)
    pt_c_wo = st.number_input("Carboidrati WO (g)", value=280)
    pt_g_wo = st.number_input("Grassi WO (g)", value=30)
    spesa_prevista_wo = st.number_input("Consumo Energetico Stimato WO (Kcal)", value=3500)
with col_pt2:
    st.markdown("### 🍏 Giorno REST")
    pt_kcal_rest = st.number_input("Target Ingestione REST (Kcal)", value=2500)
    pt_p_rest = st.number_input("Proteine REST (g)", value=200)
    pt_c_rest = st.number_input("Carboidrati REST (g)", value=180)
    pt_g_rest = st.number_input("Grassi REST (g)", value=60)
    spesa_prevista_rest = st.number_input("Consumo Energetico Stimato REST (Kcal)", value=2200)
st.write("---")


# --- SEZIONE 2: INTERRUTTORE ED INTEGRAZIONE ENERGETICA DINAMICA ---
st.subheader("🔄 Selezione Regime Giornaliero ed Energetica")
giorno_workout = st.toggle("Abilita Modalità: GIORNO WORKOUT (Attiva switch per scambiare i target energetici)", value=True)

if giorno_workout:
    target_panti = {"Kcal": pt_kcal_wo, "P": pt_p_wo, "C": pt_c_wo, "G": pt_g_wo}
    consumo_totale_stimato = spesa_prevista_wo
    st.info(f"🎯 **Target Ingestione Attivo (WORKOUT):** {target_panti['Kcal']} Kcal | P: {target_panti['P']}g | C: {target_panti['C']}g | G: {target_panti['G']}g")
else:
    target_panti = {"Kcal": pt_kcal_rest, "P": pt_p_rest, "C": pt_c_rest, "G": pt_g_rest}
    consumo_totale_stimato = spesa_prevista_rest
    st.success(f"🍏 **Target Ingestione Attivo (REST):** {target_panti['Kcal']} Kcal | P: {target_panti['P']}g | C: {target_panti['C']}g | G: {target_panti['G']}g")

st.write(f"📋 **Consumo energetico complessivo previsto dal PT per oggi:** {consumo_totale_stimato} Kcal")
bilancio_teorico = target_panti["Kcal"] - consumo_totale_stimato
if bilancio_teorico < 0:
    st.warning(f"📉 Taglio energetico programmato per oggi: Sei in deficit di {abs(bilancio_teorico)} Kcal")
else:
    st.info(f"📈 Bilancio programmato per oggi: Sei in surplus di {bilancio_teorico} Kcal")
st.write("---")


# --- SEZIONE 3: CRUSCOTTO HEALTH ED ENERGIA REALE ---
st.subheader("📊 Cruscotto Metriche Giornaliere")
col_m1, col_m2 = st.columns(2)
with col_m1:
    peso_corrente = st.number_input("Peso di Oggi (Kg)", value=91.6, step=0.1)
    ore_sonno = st.number_input("Ore di Sonno", value=8.0, step=0.5)
    passi = st.number_input("Passi Effettuati", value=10000)
    fc_media = st.number_input("❤️ Frequenza Cardiaca Media (BPM)", value=68)
with col_m2:
    distanza = st.number_input("Distanza Totale (Km)", value=7.5)
    vo2_max = st.number_input("VO2 Max Corrente", value=45.0)
    cal_attive_reali = st.number_input("Calorie Attive Reali Rilevate (Kcal)", value=600)

cal_riposo = int((10 * peso_corrente) + (6.25 * altezza) - (5 * eta) + 5)
calorie_totali_spese_reali = cal_attive_reali + cal_riposo
st.metric(label="🔥 CALORIE TOTALI REALI SPESE OGGI (Basale + Rilevate)", value=f"{calorie_totali_spese_reali} Kcal")
st.write("---")


# --- SEZIONE 4: ANATOMIA METRICA, ASIMMETRIE E PLICOMETRIA ---
st.subheader("📐 Mappe Antropometriche e Composizione Corporea")
tab1, tab2 = st.tabs(["🩸 Plicometria 3 Punti (Jackson-Pollock)", "📏 Circonferenze Muscolari (Asimmetrie)"])

with tab1:
    st.write("Inserisci le pliche millimetrate per calcolare la composizione corporea:")
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        st.info("📍 MAPPA ANATOMICA REPERE:\n\n➡️ PETTO: Plica diagonale intermedia.\n\n➡️ ADDOME: Plica verticale ombelicale.\n\n➡️ COSCIA: Plica verticale anteriore.")
    with col_pl2:
        plica_petto = st.number_input("➡️ Plica Petto (mm)", min_value=0.0, value=12.0, step=0.1)
        plica_addome = st.number_input("➡️ Plica Addome (mm)", min_value=0.0, value=18.0, step=0.1)
        plica_coscia = st.number_input("➡️ Plica Coscia (mm)", min_value=0.0, value=15.0, step=0.1)
    
    somma_pliche = plica_petto + plica_addome + plica_coscia
    if somma_pliche > 0:
        bd = 1.10938 - (0.0008267 * somma_pliche) + (0.0000016 * (somma_pliche ** 2)) - (0.0002574 * eta)
        percentuale_grasso = round(((4.95 / bd) - 4.50) * 100, 1)
        massa_grassa_kg = round((peso_corrente * percentuale_grasso) / 100, 1)
        massa_magra_kg = round(peso_corrente - massa_grassa_kg, 1)
    else:
        percentuale_grasso, massa_grassa_kg, massa_magra_kg = 0.0, 0.0, 0.0
        
    st.write("---")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric(label="📉 GRASSO CORPOREO TOTALE", value=f"{percentuale_grasso} % BF")
    with col_f2:
        st.metric(label="⚖️ Massa Grassa Stimata", value=f"{massa_grassa_kg} Kg")
    with col_f3:
        st.metric(label="💪 Massa Magra Pulita", value=f"{massa_magra_kg} Kg")

with tab2:
    st.write("Inserisci i centimetri per evidenziare le differenze tra lato destro e sinistro:")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("**🧠 Tronco e Centro**")
        c_collo = st.number_input("Collo (cm)", value=41.0)
        c_spalle = st.number_input("Spalle (cm)", value=128.0)
        c_petto = st.number_input("Petto (cm)", value=112.0)
        c_vita = st.number_input("Vita (cm)", value=86.0)
        c_fianchi = st.number_input("Fianchi (cm)", value=98.0)
    with col_c2:
        st.markdown("**🦾 Arti (Destra vs Sinistra)**")
        c_bicipite_dx = st.number_input("Bicipite DX (cm)", value=42.0)
        c_bicipite_sx = st.number_input("Bicipite SX (cm)", value=41.5)
        c_avambraccio_dx = st.number_input("Avambraccio DX (cm)", value=34.0)
        c_avambraccio_sx = st.number_input("Avambraccio SX (cm)", value=33.8)
        c_coscia_dx = st.number_input("Coscia DX (cm)", value=62.0)
        c_coscia_sx = st.number_input("Coscia SX (cm)", value=61.2)
        c_polpaccio_dx = st.number_input("Polpaccio DX (cm)", value=40.0)
        c_polpaccio_sx = st.number_input("Polpaccio SX (cm)", value=40.0)
st.write("---")


# --- SEZIONE 5: CONTATORE ACQUA INTERATTIVO ---
st.subheader("💧 Monitoraggio Idratazione")
moltiplicatore_h2o = 45 if giorno_workout else 40
target_acqua = round((peso_corrente * moltiplicatore_h2o) / 1000, 2)

col_w1, col_w2 = st.columns([1, 1.5])
with col_w1:
    st.write("Target idrico odierno:")
    if st.session_state.acqua_bevuta < target_acqua:
        st.markdown(f"<h3 style='color: #FF4B4B;'>Bevuti: {st.session_state.acqua_bevuta:.2f} / {target_acqua} L ❌</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color: #00D26A;'>Target Raggiunto! {st.session_state.acqua_bevuta:.2f} / {target_acqua} L ✓</h3>", unsafe_allow_html=True)
with col_w2:
    btn1, btn2, btn3, btn4 = st.columns(4)
    with btn1:
        if st.button("+50 ml"): st.session_state.acqua_bevuta += 0.05
    with btn2:
        if st.button("+250 ml"): st.session_state.acqua_bevuta += 0.25
    with btn3:
        if st.button("+500 ml"): st.session_state.acqua_bevuta += 0.50
    with btn4:
        if st.button("Reset 🔄"): st.session_state.acqua_bevuta = 0.0
st.write("---")


# --- SEZIONE 6: GENERATORE PASTI CASUALE UNIVERSALE ---
st.subheader("📋 Composizione Pasti Personalizzati da Dispensa")
numero_pasti = st.slider("Seleziona in quanti pasti dividere i macro di oggi:", min_value=1, max_value=6, value=5)

quota_p = int(target_panti["P"] / numero_pasti)
quota_c = int(target_panti["C"] / numero_pasti)
quota_g = int(target_panti["G"] / numero_pasti)

st.write(f"Ciascun pasto dovrà contenere: 🍗 Proteine: {quota_p}g | 🍚 Carboidrati: {quota_c}g | 🥑 Grassi: {quota_g}g")
st.write(" ")

for i in range(1, numero_pasti + 1):
    with st.container():
        st.markdown(f"### 🍽️ Pasto {i}")
        if st.button(f"🎲 Genera Combinazione per Pasto {i}", key=f"btn_univ_{i}"):
            f_carbo = [k for k, v in BANCA_DATI.items() if v["cat"] == "Carboidrati" and dispensa_attiva[k]]
            f_pro = [k for k, v in BANCA_DATI.items() if v["cat"] == "Proteine" and dispensa_attiva[k]]
            f_grassi = [k for k, v in BANCA_DATI.items() if v["cat"] == "Grassi" and dispensa_attiva[k]]
            f_verdura = [k for k, v in BANCA_DATI.items() if v["cat"] == "Verdura" and dispensa_attiva[k]]
            f_frutta = [k for k, v in BANCA_DATI.items() if v["cat"] == "Frutta" and dispensa_attiva[k]]
            
            blocchi_errore = False
            scelte_output = []
            
            if quota_c > 0 and not f_carbo:
                st.error("❌ Errore: Manca la fonte di Carboidrati in Dispensa!")
                blocchi_errore = True
            if quota_p > 0 and not f_pro:
                st.error("❌ Errore: Manca la fonte di Proteine in Dispensa!")
                blocchi_errore = True
            if quota_g > 0 and not f_grassi:
                st.error("❌ Errore: Manca la fonte di Grassi in Dispensa!")
                blocchi_errore = True
                
            if not blocchi_errore:
                if quota_c > 0:
                    c_s = random.choice(f_carbo)
                    grammi_c = int((quota_c / BANCA_DATI[c_s]["C"]) * 100)
                    scelte_output.append(f"🍚 **{grammi_c}g** di **{c_s}**")
                if quota_p > 0:
                    p_s = random.choice(f_pro)
                    grammi_p = int((quota_p / BANCA_DATI[p_s]["P"]) * 100)
                    scelte_output.append(f"🍗 **{grammi_p}g** di **{p_s}**")
                if quota_g > 0:
                    g_s = random.choice(f_grassi)
                    grammi_g = int((quota_g / BANCA_DATI[g_s]["G"]) * 100)
                    scelte_output.append(f"🥑 **{grammi_g}g** di **{g_s}**")
                
                if f_verdura and random.choice([True, False]):
                    scelte_output.append(f"🥗 *Contorno:* **{random.choice(f_verdura)}** a piacere")
                if f_frutta and random.choice([True, False]):
                    scelte_output.append(f"🍎 *Quota Frutta:* **{random.choice(f_frutta)}**")
                    
                st.success("💡 Menù calcolato dal carrello spesa:")
                for line in scelte_output:
                    st.markdown(line)
        st.write("---")
