import streamlit as st
import pandas as pd
import requests

st.title("🔮 Predicción de Compra")

file = st.file_uploader("Sube archivo CSV con columnas: edad, ingresos", type=["csv", "txt"])

if file is not None:
    df = pd.read_csv(file)
    st.write("📄 Datos cargados:")
    st.dataframe(df)

    if st.button("Ejecutar modelo"):
        datos = df.to_dict(orient="records")
        try:
            url = "https://ml-api-production.up.railway.app/predict"  # Reemplaza con tu URL real
            response = requests.post(url, json=datos)
            if response.status_code == 200:
                df["prediccion"] = response.json()["predicciones"]
                st.success("✅ Predicción completada")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Descargar resultados", csv, "resultados.csv", "text/csv")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Error conectando con la API: {e}")