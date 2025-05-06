import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime

def get_meaning(sum_value):
    meanings = {
        1: "Солнце — индивидуальность, уверенность, энергия лидерства, стремление к признанию, отцовская сила, честолюбие, творческая сила.",
        2: "Луна — чувствительность, эмоциональная глубина, интуиция, заботливость, материнская энергия, смена настроений, мягкость, мечтательность.",
        3: "Юпитер — мудрость, духовность, преподавание, вдохновение, защита, закон, наставничество, стремление к знаниям и порядку.",
        4: "Раху — нестандартное мышление, изобретательность, внезапные повороты судьбы, стремление к материальному, мистика, иллюзии, нестабильность.",
        5: "Меркурий — интеллект, гибкость, дипломатичность, коммерческая жилка, умение убеждать, остроумие, жизнерадостность, быстрая адаптация.",
        6: "Венера — любовь, красота, артистизм, чувственность, романтизм, элегантность, стремление к гармонии и удовольствию.",
        7: "Кету — интуиция, отстранённость, философичность, мистика, внутренний поиск, кармические уроки, духовный выход из мира форм.",
        8: "Сатурн — карма, дисциплина, терпение, тяжёлый труд, надёжность, стабильность, сдержанность, ответственность.",
        9: "Марс — действие, энергия, храбрость, напор, агрессия, физическая сила, защита, воинственность, страсть к победе."
    }
    while sum_value > 9:
        sum_value = sum(int(d) for d in str(sum_value))
    return sum_value, meanings.get(sum_value, "Нет интерпретации")

def draw_magic_square(square):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(patches.Rectangle((0, 0), 4, 4, linewidth=3, edgecolor='#CFA216', facecolor='none'))
    for i in range(4):
        for j in range(4):
            ax.add_patch(patches.Rectangle((j, 3 - i), 1, 1, edgecolor='black', facecolor='white', linewidth=1))
            ax.text(j + 0.5, 3.5 - i, str(square[i][j]), ha='center', va='center', fontsize=16)
    st.pyplot(fig)

st.title("Магический квадрат по дате рождения")

date_str = st.text_input("Введите дату рождения в формате ДД.ММ.ГГГГ", "21.10.1986")

try:
    date_input = datetime.strptime(date_str, "%d.%m.%Y")
    day = date_input.day
    month = date_input.month
    year = date_input.year

    first_two = int(str(year)[:2])   # 19
    last_two = int(str(year)[-2:])   # 86

    a = day
    b = month
    c = first_two
    d = last_two

    magic_square = [
        [a, b, c, d],
        [c - 1, d + 1, a - 1, b + 1],
        [d - 2, c - 2, b + 2, a + 2],
        [b + 3, a + 1, d - 1, c - 3]
    ]

    st.subheader("Магический квадрат:")
    draw_magic_square(magic_square)

    row_sum = sum(magic_square[0])
    final_sum, meaning = get_meaning(row_sum)

    st.write(f"Сумма строки: **{row_sum}**")
    st.write(f"Однозначное число: **{final_sum}**")
    st.markdown(f"**Расшифровка ({final_sum}):** {meaning}")

    st.markdown("---")
    st.markdown("🔮 **Инструкция по использованию:**")
    st.markdown(
        "Этот магический квадрат отражает структуру вашей даты рождения. "
        "Первая строка содержит ключевые числа: день, месяц и год (разделённый на две части). "
        "Используйте квадрат как личный талисман: распечатайте его, держите рядом, "
        "медитируйте на его центральную часть. Считается, что такой квадрат помогает "
        "сбалансировать внутреннюю энергию и усилить связь с собственной судьбой."
    )

except ValueError:
    st.error("Введите дату в формате ДД.ММ.ГГГГ, например: 21.10.1986")
