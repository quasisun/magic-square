
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

st.title("Магический квадрат по дате рождения")

def get_meaning(sum_value):
    meanings = {
        1: "Солнце: индивидуальность, лидерство, яркость",
        2: "Луна: интуиция, мягкость, эмоциональность",
        3: "Юпитер: духовность, знания, наставничество",
        4: "Раху: трансформация, нестабильность, загадочность",
        5: "Меркурий: интеллект, гибкость, общение",
        6: "Венера: любовь, искусство, чувственность",
        7: "Кету: отречение, мистика, свобода от материального",
        8: "Сатурн: дисциплина, труд, карма",
        9: "Марс: сила, борьба, действие"
    }
    while sum_value > 9:
        sum_value = sum(int(d) for d in str(sum_value))
    return sum_value, meanings.get(sum_value, "Нет интерпретации")

def draw_square(square):
    fig, ax = plt.subplots(figsize=(4, 4))
    table_data = [[str(cell) for cell in row] for row in square]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center', edges='closed')
    table.scale(1, 2)
    table.set_fontsize(14)
    ax.axis('off')
    st.pyplot(fig)

date_input = st.date_input("Выберите дату рождения")

if date_input:
    day = date_input.day
    month = date_input.month
    year = date_input.year

    a = day
    b = month
    c = int(str(year)[-2:])
    d = sum(int(digit) for digit in str(day) + str(month) + str(year))

    magic_square = [
        [a, b, c, d],
        [c - 1, d + 1, a - 1, b + 1],
        [d - 2, c - 2, b + 2, a + 2],
        [b + 3, a + 1, d - 1, c - 3]
    ]

    st.subheader("Магический квадрат:")
    draw_square(magic_square)

    row_sum = sum(magic_square[0])
    final_sum, meaning = get_meaning(row_sum)

    st.write(f"Сумма строки: **{row_sum}**")
    st.write(f"Однозначное число: **{final_sum}**")
    st.markdown(f"**Расшифровка:** {meaning}")
