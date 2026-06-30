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

# Inizializzazione degli stati di memoria dell'applicazione
if "acqua_bevuta" not in st.session_state:
    st.session_state.acqua_bevuta = 0.0
if "pasti_generati" not in st.session_state:
    st.session_state.pasti_generati = {}

# BANCA DATI COMPLETA DI TUTTI GLI ALIMENTI GENERICI ITALIANI
BANCA_DATI = {
    "Riso Basmati": {"P": 8.0, "C": 78.0, "G": 0.8, "Kcal": 350, "cat": "Carboidrati"},
    "Riso Integrale": {"P": 7.5, "C": 73.0, "G": 1.9, "Kcal": 341, "cat": "Carboidrati"},
    "Pasta di Semola": {"P": 12.5, "C": 71.3, "G": 1.5, "Kcal": 354, "cat": "Carboidrati"},
    "Pasta Integrale": {"P": 13.0, "C": 65.0, "G": 2.0, "Kcal": 330, "cat": "Carboidrati"},
    "Cuscus": {"P": 12.8, "C": 72.4, "G": 0.6, "Kcal": 356, "cat": "Carboidrati"},
    "Fiocchi d'Avena": {"P": 11.0, "C": 60.0, "G": 8.0, "Kcal": 366, "cat": "Carboidrati"},
    "Gallette di Riso": {"P": 7.9, "C": 81.5, "G": 1.1, "Kcal": 371, "cat": "Carboidrati"},
    "Patate": {"P": 2.1, "C": 17.9, "G": 0.1, "Kcal": 80, "cat": "Carboidrati"},
    "Petto di Pollo": {"P": 23.0, "C": 0.0, "G": 0.8, "Kcal": 100, "cat": "Proteine"},
    "Fesa di Tacchino": {"P": 24.0, "C": 0.0, "G": 1.2, "Kcal": 107, "cat": "Proteine"},
    "Filetto di Manzo": {"P": 20.5, "C": 0.0, "G": 3.5, "Kcal": 114, "cat": "Proteine"},
    "Merluzzo / Nasello": {"P": 17.0, "C": 0.0, "G": 0.3, "Kcal": 71, "cat": "Proteine"},
    "Salmone": {"P": 20.0, "C": 0.0, "G": 13.0, "Kcal": 197, "cat": "Proteine"},
    "Tonno al Naturale": {"P": 25.0, "C": 0.0, "G": 0.5, "Kcal": 104, "cat": "Proteine"},
    "Albume d'Uovo": {"P": 11.0, "C": 0.7, "G": 0.2, "Kcal": 52, "cat": "Proteine"},
    "Uovo Intero": {"P": 12.4, "C": 0.0, "G": 8.7, "Kcal": 128, "cat": "Proteine"},
    "Yogurt Greco 0%": {"P": 10.3, "C": 3.0, "G": 0.0, "Kcal": 53, "cat": "Proteine"},
    "Olio Extra Vergine d'Oliva": {"P": 0.0, "C": 0.0, "G": 99.0, "Kcal": 899, "cat": "Grassi"},
    "Mandorle": {"P": 22.0, "C": 4.6, "G": 50.0, "Kcal": 579, "cat": "Grassi"},
    "Zucchine": {"P": 1.3, "C": 1.4, "G": 0.1, "Kcal": 11, "cat": "Verdura"},
    "Spinaci": {"P": 3.4, "C": 0.6, "G": 0.7, "Kcal": 23, "cat": "Verdura"},
    "Mela": {"P": 0.3, "C": 14.0, "G": 0.2, "Kcal": 52, "cat": "Frutta"}
}

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
for cibo in BANCA_DATI.keys():
    dispensa_attiva[cibo] = st.sidebar.checkbox(cibo, value=True, key=f"disp_{cibo}")

st.sidebar.write("---")
st.sidebar.subheader("Configurazione Avanzata Macro Pasti")
numero_pasti = st.sidebar.slider("Seleziona numero di pasti:", min_value=1, max_value=7, value=5)

macro_pasti_personalizzati = {}
for i in range(1, numero_pasti + 1):
    with st.sidebar.expander(f"Imposta Macro Pasto {i}"):
        p_pasto = st.number_input(f"Proteine (g) - P{i}", value=40, key=f"p_p_{i}")
        c_pasto = st.number_input(f"Carboidrati (g) - P{i}", value=50, key=f"c_p_{i}")
        g_pasto = st.number_input(f"Grassi (g) - P{i}", value=10, key=f"g_p_{i}")
        macro_pasti_personalizzati[i] = {"P": p_pasto, "C": c_pasto, "G": g_pasto}

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
    fabbisogno_corrente = pt_kcal_wo
    consumo_corrente = spesa_prevista_wo
else:
    regime_testo = "REST"
    fabbisogno_corrente = pt_kcal_rest
    consumo_corrente = spesa_prevista_rest

# Scritta del giorno monumentale centrata
st.markdown(f"<h2 style='text-align: center; letter-spacing: 2px; color: #00D26A;'>{regime_testo}</h2>", unsafe_allow_html=True)

# Calcolo Bilancio Energetico richiesto
bilancio = fabbisogno_corrente - consumo_corrente

# Cruscotto principale racchiuso in un riquadro evidenziato
st.markdown("<div style='border: 1px solid #444; padding: 20px; border-radius: 10px; background-color: #1a1a1a;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Fabbisogno", value=f"{fabbisogno_corrente} Kcal")
with col2:
    st.metric(label="Consumo Stimato", value=f"{consumo_corrente} Kcal")
with col3:
    if bilancio < 0:
        st.metric(label="Risultato", value=f"Deficit {bilancio} Kcal")
    else:
        st.metric(label="Risultato", value=f"+{bilancio} Kcal")
st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# Inserimento Dati Giornalieri Manuali ordinati
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

# Sezione Fisico con diciture accorciate per non tagliare lo schermo dello smartphone
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
        c_collo = st.number_input("Collo (cm)", value=41.0)
        c_spalle = st.number_input("Spalle (cm)", value=128.0)
        c_petto = st.number_input("Petto (cm)", value=112.0)
        c_vita = st.number_input("Vita (cm)", value=86.0)
    with col_c2:
        c_bicipite_dx = st.number_input("Bicipite DX (cm)", value=42.0)
        c_coscia_dx = st.number_input("Coscia DX (cm)", value=62.0)
        c_polpaccio_dx = st.number_input("Polpaccio DX (cm)", value=40.0)

st.write("---")

# --- FUNZIONE LOGICA GENERATORE PASTI AVANZATO ---
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
    
    return [
        {"alimento": fonte_c, "grammi": gr_c, "macro": f"C: {target_c}g"},
        {"alimento": fonte_p, "grammi": gr_p, "macro": f"P: {target_p}g"},
        {"alimento": fonte_g, "grammi": gr_g, "macro": f"G: {target_g}g"}
    ]

st.markdown("<h3 style='text-align: center;'>Pianificazione Alimentare Giornaliera</h3>", unsafe_allow_html=True)

# Tasto di generazione globale per tutti i pasti impostati
if st.button("Genera Tutti i Pasti", use_container_width=True, type="primary"):
    for idx in range(1, numero_pasti + 1):
        target = macro_pasti_personalizzati.get(idx, {"P": 40, "C": 50, "G": 10})
        st.session_state.pasti_generati[idx] = genera_singolo_pasto(target["P"], target["C"], target["G"])

# Rendering dinamico e controllo dei singoli pasti
for idx in range(1, numero_pasti + 1):
    st.markdown(f"#### Pasto {idx}")
    
    col_pasto_sx, col_pasto_dx = st.columns([2, 1])
    
    with col_pasto_sx:
        if idx in st.session_state.pasti_generati:
            for ingrediente in st.session_state.pasti_generati[idx]:
                st.write(f"• **{ingrediente['alimento']}**: {ingrediente['grammi']}g ({ingrediente['macro']})")
        else:
            st.info("Pasto non ancora generato.")
            
    with col_pasto_dx:
        riferimento = st.selectbox("Riferimento", ["Default", "Workout", "Rest", "Extra"], key=f"ref_{idx}", label_visibility="collapsed")
        if st.button("Rigenera questo", key=f"regen_{idx}", use_container_width=True):
            if riferimento == "Workout":
                target = {"P": 50, "C": 70, "G": 5} # Valori teorici forzati WO
            elif riferimento == "Rest":
                target = {"P": 40, "C": 30, "G": 15} # Valori teorici forzati REST
            elif riferimento == "Extra":
                target = {"P": 20, "C": 100, "G": 30} # Valori teorici Extra
            else:
                target = macro_pasti_personalizzati.get(idx, {"P": 40, "C": 50, "G": 10})
                
            st.session_state.pasti_generati[idx] = genera_singolo_pasto(target["P"], target["C"], target["G"])
            st.rerun()
    st.write("---")
