import io
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime

st.set_page_config(page_title="Магический квадрат", page_icon="🔢", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cormorant Garamond', Georgia, serif;
    }

    .main { background-color: #0e0e0e; }

    h1 { color: #CFA216 !important; text-align: center; letter-spacing: 2px; }
    h2, h3 { color: #CFA216 !important; }

    .stTextInput > label { color: #d4af6a; font-size: 1rem; }
    .stTextInput > div > input {
        background-color: #1a1a1a;
        color: #f5e6c8;
        border: 1px solid #CFA216;
        border-radius: 4px;
    }

    .result-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #111 100%);
        border: 1px solid #CFA216;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
        color: #f5e6c8;
    }

    .planet-badge {
        display: inline-block;
        background: #CFA216;
        color: #0e0e0e;
        font-weight: 600;
        padding: 2px 14px;
        border-radius: 20px;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }

    .number-large {
        font-size: 3rem;
        font-weight: 600;
        color: #CFA216;
        line-height: 1;
    }

    .divider {
        border: none;
        border-top: 1px solid #333;
        margin: 1.2rem 0;
    }

    .stExpander {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }

    .stExpander summary { color: #d4af6a !important; }

    .stDownloadButton > button {
        background-color: transparent;
        border: 1px solid #CFA216;
        color: #CFA216;
        border-radius: 4px;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background-color: #CFA216;
        color: #0e0e0e;
    }
</style>
""", unsafe_allow_html=True)

PLANET_MEANINGS = {
    1: ("Солнце", "☀️", "Индивидуальность, уверенность, энергия лидерства, стремление к признанию, "
        "отцовская сила, честолюбие, творческая сила."),
    2: ("Луна", "🌙", "Чувствительность, эмоциональная глубина, интуиция, заботливость, "
        "материнская энергия, смена настроений, мягкость, мечтательность."),
    3: ("Юпитер", "♃", "Мудрость, духовность, преподавание, вдохновение, защита, закон, "
        "наставничество, стремление к знаниям и порядку."),
    4: ("Раху", "☊", "Нестандартное мышление, изобретательность, внезапные повороты судьбы, "
        "стремление к материальному, мистика, иллюзии, нестабильность."),
    5: ("Меркурий", "☿", "Интеллект, гибкость, дипломатичность, коммерческая жилка, "
        "умение убеждать, остроумие, жизнерадостность, быстрая адаптация."),
    6: ("Венера", "♀", "Любовь, красота, артистизм, чувственность, романтизм, элегантность, "
        "стремление к гармонии и удовольствию."),
    7: ("Кету", "☋", "Интуиция, отстранённость, философичность, мистика, внутренний поиск, "
        "кармические уроки, духовный выход из мира форм."),
    8: ("Сатурн", "♄", "Карма, дисциплина, терпение, тяжёлый труд, надёжность, "
        "стабильность, сдержанность, ответственность."),
    9: ("Марс", "♂", "Действие, энергия, храбрость, напор, агрессия, физическая сила, "
        "защита, воинственность, страсть к победе."),
}


def digital_root(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def build_square(day, month, year):
    a = day
    b = month
    c = int(str(year)[:2])
    d = int(str(year)[-2:])
    return [
        [a,     b,     c,     d    ],
        [c - 1, d + 1, a - 1, b + 1],
        [d - 2, c - 2, b + 2, a + 2],
        [b + 3, a + 1, d - 1, c - 3],
    ]


def render_square(square):
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('#0e0e0e')
    ax.set_facecolor('#0e0e0e')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(patches.Rectangle(
        (0, 0), 4, 4,
        linewidth=3, edgecolor='#CFA216', facecolor='none'
    ))

    for i in range(4):
        for j in range(4):
            ax.add_patch(patches.Rectangle(
                (j, 3 - i), 1, 1,
                edgecolor='#CFA216', facecolor='#1a1a1a', linewidth=0.8
            ))
            ax.text(
                j + 0.5, 3.5 - i, str(square[i][j]),
                ha='center', va='center',
                fontsize=18, color='#f5e6c8',
                fontfamily='serif'
            )
    return fig


# ── UI ────────────────────────────────────────────────────────────────────────

st.markdown("<h1>Магический квадрат</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#888;font-size:1rem;margin-top:-0.5rem;'>"
    "Расчёт по дате рождения · Ведическая нумерология</p>",
    unsafe_allow_html=True
)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

date_str = st.text_input("Дата рождения (ДД.ММ.ГГГГ)", placeholder="например: 21.10.1986")

try:
    if not date_str.strip():
        st.stop()

    date_obj = datetime.strptime(date_str.strip(), "%d.%m.%Y")
    day, month, year = date_obj.day, date_obj.month, date_obj.year

    square = build_square(day, month, year)
    row_sum = sum(square[0])
    root = digital_root(row_sum)
    planet, symbol, description = PLANET_MEANINGS[root]

    # ── квадрат ──────────────────────────────────────────────────────────────
    col_sq, col_info = st.columns([1, 1], gap="large")

    with col_sq:
        fig = render_square(square)
        st.pyplot(fig, use_container_width=True)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight",
                    facecolor='#0e0e0e')
        buf.seek(0)
        plt.close(fig)

        st.download_button(
            label="Скачать квадрат",
            data=buf,
            file_name=f"magic_square_{date_str.replace('.', '_')}.png",
            mime="image/png",
        )

    with col_info:
        st.markdown(f"""
        <div class='result-card'>
            <div style='color:#888;font-size:0.9rem;margin-bottom:0.3rem;'>
                Сумма первой строки
            </div>
            <div class='number-large'>{row_sum}</div>
            <div style='color:#888;font-size:0.85rem;margin-top:0.3rem;'>
                → однозначное: <strong style='color:#f5e6c8;'>{root}</strong>
            </div>
        </div>
        <div class='result-card' style='margin-top:0.6rem;'>
            <div class='planet-badge'>{symbol} {planet}</div>
            <p style='margin:0.6rem 0 0;color:#d4af6a;line-height:1.6;'>
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── ключи квадрата ────────────────────────────────────────────────────────
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    with st.expander("Ключи квадрата — откуда берутся числа"):
        st.markdown(f"""
| Ячейка | Значение | Число |
|--------|----------|-------|
| **A** | День рождения | {day} |
| **B** | Месяц | {month} |
| **C** | Первые две цифры года (век) | {int(str(year)[:2])} |
| **D** | Последние две цифры года | {int(str(year)[-2:])} |

Остальные ячейки вычисляются по формуле: строки 2–4 строятся
на основе A, B, C, D со сдвигами ±1, ±2, ±3.
        """)

    with st.expander("Как использовать этот квадрат"):
        st.markdown("""
Этот квадрат отражает структуру вашей даты рождения.
Первая строка — четыре ключевых числа: день, месяц и год (разделённый на две части).

**Практическое применение:**
- Распечатайте и заламинируйте или перенесите на дерево, бумагу, ткань.
- Раскрасьте в цвета планет ведической нумерологии или интуитивно.
- Разместите на рабочем столе, у алтаря, используйте для медитации.

За подробной расшифровкой обращайтесь к нумерологу.
        """)

except ValueError:
    st.error("Введите дату в формате ДД.ММ.ГГГГ, например: 21.10.1986")
