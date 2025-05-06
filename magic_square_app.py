
import streamlit as st
from datetime import datetime

st.title("Магический квадрат по дате рождения")

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
    for row in magic_square:
        st.write("  ".join(str(num).rjust(3) for num in row))
