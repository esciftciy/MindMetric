import streamlit as st
import pandas as pd
import numpy as np
import time
import math
import plotly.graph_objects as go

# Sayfa Yapılandırması
st.set_page_config(
    page_title="MindMetric - Kişisel Keşif & Yaşam Analizi", 
    page_icon="🧠", 
    layout="centered"
)

# Kategori İsimleri (5 Temel Yaşam Boyutu)
CATEGORY_NAMES = {
    0: "Kriz, Stres & Duygu Yönetimi",
    1: "Aşk, Bağlanma & Romantik İlişkiler",
    2: "Aile Dinamikleri & Derin Bağlar",
    3: "Kariyer, Hırs & Gelecek Vizyonu",
    4: "Sosyal Uyum & Arkadaşlık Mimarisi"
}

# DOĞRUDAN KOD İÇİNE GÖMÜLÜ SORU VERİ SETİ (CSV Bağımsız)
QUESTIONS_DATA = [
    # Category 0: Kriz, Stres & Duygu Yönetimi
    {"id": 101, "category": 0, "text": "Önemli bir projenin/işin teslimine 2 saat kala telafisi zor bir hata fark ettiniz. İlk tepkiniz ne olur?", "opt0": "Dürüstçe durumu bildirip ek süre talep ederim", "opt1": "Hatayı geçici bir yamayla kapatıp fark edilmemesini umarım", "opt2": "Ekip üzerinde baskı kurup durmaksızın düzeltmeye çalışırım", "opt3": "Sorumluluğu başkalarına veya talihsizliğe atarım", "correct": 0, "difficulty": 2.0},
    {"id": 102, "category": 0, "text": "Yüksek stres ve belirsizlik altında çalışırken zihinsel dengenizi nasıl korursunuz?", "opt0": "Kontrol edebildiğim değişkenlere odaklanıp belirsizliği kabul ederim", "opt1": "Tüm olumsuz senaryoları zihnimde sürekli simüle ederim", "opt2": "Duygularımı tamamen bastırıp sadece göreve odaklanırım", "opt3": "İşleri akışına bırakıp sonucun ortaya çıkmasını beklerim", "correct": 0, "difficulty": 3.5},
    {"id": 103, "category": 0, "text": "Batmaya yakın ve büyük emek verilmiş bir projeye devam etme kararı alırken tutumunuz ne olur?", "opt0": "Zararı kabul edip yatırımı/emeği derhal durdururum", "opt1": "Kurtulma şansı düşük de olsa devam etmek için risk alırım", "opt2": "Kararı geciktirip durumun kendiliğinden düzelmesini beklerim", "opt3": "Sorumluluğu başkasına atarım", "correct": 0, "difficulty": 4.5},
    {"id": 104, "category": 0, "text": "Hayati bir karar alırken sezgilerinize mi yoksa rasyonel verilere mi güvenirsiniz?", "opt0": "Verileri temel alır ancak sezgilerimi son kontrol mekanizması yaparım", "opt1": "Sadece somut veriye dayanır sezgileri tamamen yok sayarım", "opt2": "Sadece iç güdüme ve hislerime güvenirim", "opt3": "Karar vermekte zorlanır kararı başkasına bırakırım", "correct": 0, "difficulty": 4.8},
    
    # Category 1: Aşk, Bağlanma & Romantik İlişkiler
    {"id": 201, "category": 1, "text": "Romantik bir ilişkide anlaşmazlık çıktığında ilk iletişim refleksiniz ne olur?", "opt0": "Sakinleşip mantık çerçevesinde duygu ve düşüncelerimi dürüstçe ifade ederim", "opt1": "Kırgınlığımı belli etmek için geri çekilir ve partnerimin anlamasını beklerim", "opt2": "Tartışmayı o an kazanmak için savunmaya ve karşı taarruza geçerim", "opt3": "Gerginlikten kaçınmak için kendi haklılığımdan feragat eder konuyu kapatırım", "correct": 0, "difficulty": 2.0},
    {"id": 202, "category": 1, "text": "Sevgiliniz/Eşiniz zor bir dönemden geçerken ona nasıl destek olursunuz?", "opt0": "Çözüm üretmek yerine önce sadece dinler ve duygusal varlığımı hissettiririm", "opt1": "Hemen pratik tavsiyeler verip problemi onun adına çözmeye çalışırım", "opt2": "Kendi kaygılarım artar ve ne yapacağımı bilemeyip mesafeli kalırım", "opt3": "Durumu abarttığını düşünüp neşelenmesi için konuyu değiştiririm", "correct": 0, "difficulty": 3.5},
    {"id": 203, "category": 1, "text": "Aşkta en çok aradığınız ve vazgeçilmez bulduğunuz temel duygu nedir?", "opt0": "Ruhsal derinlik, dürüstlük ve koşulsuz güven", "opt1": "Tutku, heyecan ve sürekli yenilik", "opt2": "Huzur, konfor ve stabilite", "opt3": "Birlikte yüksek hedeflere ulaşma ve güç birliği", "correct": 0, "difficulty": 4.5},
    {"id": 204, "category": 1, "text": "İlişkide alanınıza ve bağımsızlığınıza müdahale edildiğinde nasıl tepki verirsiniz?", "opt0": "Sınırlarımı net ve nazik bir dille çizer özgürlüğüme sahip çıkarım", "opt1": "Partnerimi kırmamak için sınırlarımın ihlal edilmesine izin veririm", "opt2": "Aşırı tepki gösterip ilişkiyi bitirme noktasına getiririm", "opt3": "İçime atar ancak zamanla partnerime karşı soğurum", "correct": 0, "difficulty": 4.8},

    # Category 2: Aile Dinamikleri & Derin Bağlar
    {"id": 301, "category": 2, "text": "Kök ailenizle (anne/baba/kardeş) aranızdaki kişisel sınırları nasıl korursunuz?", "opt0": "Kendi yetişkin bireyselliğimi korur sevgi dolu ama net sınırlar çizerim", "opt1": "Ailename hayır diyemez kendi kararlarımda bile onların onayını ararım", "opt2": "Çatışmamak için mesafeli durur duygusal bağımı koparma noktasına getiririm", "opt3": "Tüm hayatımın detaylarını yönetmelerine izin veririm", "correct": 0, "difficulty": 2.0},
    {"id": 302, "category": 2, "text": "Aile içi bir kriz veya tartışma yaşandığında rolünüz ne olur?", "opt0": "Sakin kalıp arabuluculuk yapar tarafları dinleyerek ortamı yumuşatırım", "opt1": "Taraf tutar ve kendi fikrimi agresifçe savunurum", "opt2": "Ortamdan kaçar ve konu kapanana kadar sessiz kalırım", "opt3": "Olayı dramatikleştirip ilgiyi kendi üzerime çekerim", "correct": 0, "difficulty": 3.5},
    {"id": 303, "category": 2, "text": "Ailenizin sizden beklentileri ile kendi hayalleriniz çeliştiğinde ne yaparsınız?", "opt0": "Ailemin fikirlerine saygı duyar ancak kendi yolumu kararlılıkla çizerim", "opt1": "Ailemi hayal kırıklığına uğratmamak için kendi isteklerimden vazgeçerim", "opt2": "Ailemle bağları koparma pahasına isyan eder sert tepki veririm", "opt3": "Kendi hayallerimi gizlice yaşamaya çalışırım", "correct": 0, "difficulty": 4.5},

    # Category 3: Kariyer, Hırs & Gelecek Vizyonu
    {"id": 401, "category": 3, "text": "Kariyerinizde ve iş hayatınızda sizi harekete geçiren ana motor nedir?", "opt0": "Üretmek, iz bırakmak ve kişisel potansiyelimi en üste çıkarmak", "opt1": "Finansal güç, konforlu bir yaşam ve prestij", "opt2": "Toplumda saygınlık kazanmak ve takdir edilmek", "opt3": "Sadece geçimimi sağlamak ve güvende olmak", "correct": 0, "difficulty": 2.0},
    {"id": 402, "category": 3, "text": "İş hayatında büyük bir fırsat ama aynı zamanda büyük bir başarısızlık riski var. Ne yaparsınız?", "opt0": "Risk analizi yapar, avantajlar ağır basıyorsa cesurca adıma geçerim", "opt1": "Güvenli alanımda kalır riskli fırsatları reddederim", "opt2": "Hesapsızca atlar sonucu ne olursa olsun denerim", "opt3": "Kararı bir akıl hocasına veya yöneticime bırakırım", "correct": 0, "difficulty": 3.5},
    {"id": 403, "category": 3, "text": "İş/Okul ortamında haksızlığa veya adaletsizliğe uğradığınızda tepkiniz ne olur?", "opt0": "Profesyonel sınırlar içinde hakkımı sonuna kadar ararım", "opt1": "Sessiz kalır ama içten içe kuruma/insanlara karşı aidiyetimi kaybederim", "opt2": "Agresif tepki verir ve ortalığı ayağa kaldırırım", "opt3": "İşi/okulu bırakma noktasına gelir pes ederim", "correct": 0, "difficulty": 4.5},

    # Category 4: Sosyal Uyum & Arkadaşlık Mimarisi
    {"id": 501, "category": 4, "text": "Yeni girdiğiniz bir sosyal ortamda veya toplulukta kendinizi nasıl konumlarsınız?", "opt0": "Gözlem yapar, doğal bir akışla insanlarla iletişime geçerim", "opt1": "Ortamın odak noktası olmaktan keyif alır, sohbeti başlatırım", "opt2": "Kenarda kalmayı tercih eder, birinin benimle konuşmasını beklerim", "opt3": "Aşırı yüzeysel bulursam ortamdan hemen ayrılırım", "correct": 0, "difficulty": 2.0},
    {"id": 502, "category": 4, "text": "Bir dostunuz hayati bir hata yaptığında tutumunuz ne olur?", "opt0": "Dostluğumu korur ama yaptığı hatayı yüzüne dürüstçe söylerim", "opt1": "Onu kaybetmemek için hatasını görmezden gelir, koşulsuz desteklerim", "opt2": "Ondan hemen soğur ve dostluğumu bitiririm", "opt3": "Hatayı başkalarına anlatıp durumu gıybet konusu yaparım", "correct": 0, "difficulty": 3.5},
    {"id": 503, "category": 4, "text": "İnsan ilişkilerinde sınırlarınız ihlal edildiğinde nasıl tepki verirsiniz?", "opt0": "Sınırımı net ve saygılı bir dille ifade eder, tekrarlanırsa mesafe koyarım", "opt1": "Sessiz kalır, içimde biriktirir ve günün birinde patlarım", "opt2": "Agresif bir dille karşı tarafı suçlarım", "opt3": "Sınır kavramını önemsemem, her şeyi akışına bırakırım", "correct": 0, "difficulty": 4.5}
]

questions_df = pd.DataFrame(QUESTIONS_DATA)

# --- ÖZEL MODERN CSS STİLLERİ ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(120deg, #2A2A72, #009FFD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4A5568;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.6);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
        color: white;
        border: none;
        padding: 14px 28px;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(142, 84, 233, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(142, 84, 233, 0.4);
        color: white;
    }
    div[role="radiogroup"] > label {
        background: white;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 2px solid #E2E8F0;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    div[role="radiogroup"] > label:hover {
        border-color: #8E54E9;
        background: #F7FAFC;
    }
    </style>
""", unsafe_allow_html=True)

# Sigmoid IRT Hesaplaması
def calculate_expected(ability, difficulty):
    return 1.0 / (1.0 + math.exp(-(ability - difficulty)))

# Seviye ve Reaksiyon Süresi Güncellemesi
def update_ability(current_ability, difficulty, is_correct, response_time):
    expected = calculate_expected(current_ability, difficulty)
    response = 1.0 if is_correct else 0.0
    
    time_factor = 1.0
    if is_correct:
        if response_time < 6.0:
            time_factor = 1.25
        elif response_time > 20.0:
            time_factor = 0.85
    else:
        if response_time < 3.0:
            time_factor = 1.35
            
    k_factor = 0.6 * time_factor
    new_ability = current_ability + k_factor * (response - expected)
    return max(1.0, min(5.0, new_ability))

# Oturum Durumları
if "step" not in st.session_state:
    st.session_state.step = "welcome"
    st.session_state.abilities = {i: 3.0 for i in range(5)}
    st.session_state.correct_counts = {i: 0 for i in range(5)}
    st.session_state.total_counts = {i: 0 for i in range(5)}
    st.session_state.response_times = {i: [] for i in range(5)}
    st.session_state.current_cat = 0
    st.session_state.current_q_step = 1
    st.session_state.asked_ids = []

# --- 1. AŞAMA: GİRİŞ EKRANI ---
if st.session_state.step == "welcome":
    st.markdown('<div class="main-title">🧠 MindMetric</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Kişisel Keşif, İlişkiler & Derin Yaşam Profilleme</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #2D3748; margin-top: 0;">✨ Kendinizi Keşfetmeye Hoş Geldiniz</h4>
        <p style="color: #4A5568; line-height: 1.6;">
        Bu platform; matematik kalıplarından uzak, tamamen <b>karakteriniz, duygu dünyanız, ilişkileriniz ve yaşam tercihleriniz</b> üzerine odaklanmış gelişmiş bir psikometrik analiz sunar.
        </p>
        <ul style="color: #4A5568; padding-left: 20px; line-height: 1.8;">
            <li>❤️ <b>Aşk & Bağlanma:</b> İlişki dinamikleri ve sevgi dili</li>
            <li>🏡 <b>Aile & Sınırlar:</b> Kök aile bağları ve aidiyet</li>
            <li>💼 <b>Kariyer & Vizyon:</b> Hırs, başarı ve gelecek algısı</li>
            <li>🤝 <b>Sosyal Uyum:</b> Dostluk, güven ve iletişim stili</li>
            <li>🛡️ <b>Kriz Yönetimi:</b> Stres toleransı ve duygusal olgunluk</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    user_name = st.text_input("Adınız Soyadınız:", value="Sude")
    if st.button("Kişisel Değerlendirmeyi Başlat 🚀"):
        st.session_state.user_name = user_name
        st.session_state.step = "testing"
        st.session_state.q_start_time = time.time()
        st.rerun()

# --- 2. AŞAMA: DİNAMİK TEST EKRANI ---
elif st.session_state.step == "testing":
    cat = st.session_state.current_cat
    
    cat_qs = questions_df[(questions_df["category"] == cat) & (~questions_df["id"].isin(st.session_state.asked_ids))]
    
    if cat_qs.empty or st.session_state.current_q_step > 3:
        if cat < 4:
            st.session_state.current_cat += 1
            st.session_state.current_q_step = 1
            st.rerun()
        else:
            st.session_state.step = "result"
            st.rerun()
            
    user_ab = st.session_state.abilities[cat]
    cat_qs = cat_qs.copy()
    cat_qs["diff_delta"] = (cat_qs["difficulty"] - user_ab).abs()
    selected_q = cat_qs.sort_values("diff_delta").iloc[0]
    
    # İlerleme Çubuğu & Başlık
    progress_val = (cat * 3 + st.session_state.current_q_step) / 15
    st.progress(progress_val)
    st.caption(f"Boyut {cat + 1}/5: **{CATEGORY_NAMES[cat]}** | Soru {st.session_state.current_q_step}/3")
    
    # Soru Kartı
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #1A202C; margin-top: 0; font-weight: 700; font-size: 1.2rem;">
            {selected_q['text']}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    options = [selected_q["opt0"], selected_q["opt1"], selected_q["opt2"], selected_q["opt3"]]
    choice = st.radio("Cevabınızı Seçiniz:", options, index=None, label_visibility="collapsed")
    
    st.write("")
    if st.button("Cevabı Onayla ve İlerle ➡"):
        if choice is None:
            st.warning("Lütfen bir seçeneği işaretleyin!")
        else:
            elapsed = time.time() - st.session_state.q_start_time
            chosen_idx = options.index(choice)
            is_correct = (chosen_idx == selected_q["correct"])
            
            st.session_state.abilities[cat] = update_ability(user_ab, selected_q["difficulty"], is_correct, elapsed)
            st.session_state.asked_ids.append(selected_q["id"])
            st.session_state.total_counts[cat] += 1
            if is_correct:
                st.session_state.correct_counts[cat] += 1
            st.session_state.response_times[cat].append(elapsed)
            
            st.session_state.current_q_step += 1
            st.session_state.q_start_time = time.time()
            st.rerun()

# --- 3. AŞAMA: SONUÇ VE DERİN KİŞİLİK RAPORU ---
elif st.session_state.step == "result":
    st.balloons()
    st.markdown('<div class="main-title">🎯 MindMetric Yaşam Haritası</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">Katılımcı: <b>{st.session_state.user_name}</b></div>', unsafe_allow_html=True)
    
    scores_100 = [((st.session_state.abilities[i] - 1.0) / 4.0) * 100 for i in range(5)]
    categories = [CATEGORY_NAMES[i] for i in range(5)]
    
    # RADAR CHART
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_100 + [scores_100[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(142, 84, 233, 0.25)',
        name='Yaşam Dengesi',
        line=dict(color='#8E54E9', width=3)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E2E8F0'),
            angularaxis=dict(gridcolor='#E2E8F0')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PSİKOLOJİK DERİN ÇIKARIMLAR
    st.subheader("🧬 Kişisel & Duygusal Profil Özeti")
    
    ask_score = scores_100[1]
    kariyer_score = scores_100[3]
    
    if ask_score >= 70:
        ask_analiz = "❤️ <b>Güvenli Bağlanan & Şeffaf:</b> İlişkilerde iletişime, derinliğe ve karşılıklı özgürlüğe değer veriyorsunuz. Duygularınızı açıkça ifade etmekten korkmuyorsunuz."
    else:
        ask_analiz = "🛡️ <b>Tedbirli & Korumacı:</b> Aşkta kendinizi koruma dürtünüz ön planda. Tamamen güvenmeden önce savunma duvarlarınızı aşamalı olarak indiriyorsunuz."
        
    if kariyer_score >= 70:
        kariyer_analiz = "🚀 <b>Vizyoner & Hırslı:</b> Kendi yolunu çizmeyi seven, risk alabilen ve iz bırakma arzusu yüksek bir yapıya sahipsiniz."
    else:
        kariyer_analiz = "⚖️ <b>Dengeli & Huzur Odaklı:</b> İş hayatını yaşamın amacı değil bir aracı olarak görüyorsunuz. Huzur ve konfor alanınız sizin için yüksek hırslardan daha kıymetli."

    st.markdown(f"""
    <div class="metric-card" style="border-left: 5px solid #8E54E9;">
        <h4 style="margin-top:0; color: #2D3748;">Aşk & İlişki Dinamiğiniz</h4>
        <p style="color: #4A5568; font-size: 1rem;">{ask_analiz}</p>
        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
        <h4 style="margin-top:0; color: #2D3748;">Kariyer & Yaşam Felsefeniz</h4>
        <p style="color: #4A5568; font-size: 1rem;">{kariyer_analiz}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # METRİKLER VE PERFORMANS
    st.subheader("📈 Boyut Bazlı Uyum Puanları")
    for i in range(5):
        st.write(f"**{CATEGORY_NAMES[i]}**")
        st.progress(scores_100[i] / 100)
        st.caption(f"Denge Puanı: {scores_100[i]:.1f} / 100")
        st.divider()
        
    if st.button("Yeni Değerlendirme Başlat 🔄"):
        st.session_state.clear()
        st.rerun()