import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('***RESIDUOS MUNICIPALES GENERADOS ANUALMENTE***')
# Subtítulo en el medio
st.subheader("Residuos municipales generados por periodo y región")
# Texto normal
st.write("En el Perú, la gestión eficiente de los residuos sólidos municipales es un desafío prioritario. Esta página web presenta los datos de generación anual de residuos municipales para las 24 regiones del país, información fundamental para desarrollar políticas y estrategias de recolección, transporte, tratamiento y disposición final adecuados. Los datos provienen de informes técnicos y estadísticas oficiales del Ministerio del Ambiente y otras entidades, y serán actualizados periódicamente para brindar un panorama confiable sobre la situación de los residuos sólidos a nivel regional y nacional.")

csv_file = r"C:\Users\hp\Documents\PROGRAMACION\PROYECTO 2024\Residuos municipales generados anualmente (1).csv"

encodings = ['utf-8', 'latin1', 'utf-16', 'cp1252']
for encoding in encodings:
    try:
        df = pd.read_csv(csv_file, encoding=encoding , sep=';')
        break  
    except:
        continue  
st.write(df)

