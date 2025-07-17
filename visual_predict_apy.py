import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Prediksi & Visualisasi", layout="wide")
st.title("📈 Prediksi & Visualisasi Status Mesin")

file = st.file_uploader("Upload File Excel (.xlsx)", type="xlsx")

if file:
    df = pd.read_excel(file)

    st.subheader("📝 Edit Data")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if 'status' in edited_df.columns:
        X = edited_df.drop(columns='status')
        y = edited_df['status']

        model = DecisionTreeClassifier()
        model.fit(X, y)
        st.success("✅ Model berhasil dilatih dari data yang sudah diedit!")

        if st.button("🔍 Prediksi Semua Baris"):
            pred = model.predict(X)
            edited_df['status'] = pred
            st.dataframe(edited_df, use_container_width=True)

            hasil_excel = edited_df.to_excel(index=False, engine="openpyxl")
            st.download_button("📥 Download Hasil Prediksi", data=hasil_excel, file_name="hasil_prediksi.xlsx")

        # --- Visualisasi ---
        st.subheader("📊 Visualisasi Data")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribusi Status (Pie Chart)")
            status_count = edited_df['status'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(status_count, labels=status_count.index, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.markdown("#### Tren Suhu, Arus, Tegangan (Line Chart)")
            fig2, ax2 = plt.subplots()
            sns.lineplot(data=edited_df.drop(columns='status'), ax=ax2)
            ax2.set_xlabel("Index")
            ax2.set_ylabel("Nilai Sensor")
            st.pyplot(fig2)

    else:
        st.error("❌ Kolom 'status' tidak ditemukan dalam data.")
