import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np

def load_dataset() :
    # Dictionary kosong untuk menyimpan data setiap kota
    dfs = {}
    for file_name in os.listdir("./dashboard/dataset") :
        # Load dataset
        dfs[file_name.replace('.csv', '')] = pd.read_csv(f"./dashboard/dataset/{file_name}")

    for k, df in dfs.items() :
        dfs[k].set_index('datetime', inplace=True)

    return dfs

def count_avg_temp(start_year, end_year, city) :
    global dfs
    mean_summer, mean_winter = 0, 0

    for year in range(start_year, end_year+1) :
        mean_summer += dfs[city][f"{year}-06-01":f"{year}-08-31"]['TEMP'].mean()
        mean_winter += dfs[city][f"{year}-12-01":f"{(year+1)}-02-28"]['TEMP'].mean()

    mean_summer /= (end_year - start_year)+1
    mean_winter /= (end_year - start_year)+1

    return mean_summer, mean_winter

def temperature_graph(start_year, end_year, city) :
    global dfs
    # Inisialisasi plot
    fig, ax = plt.subplots(figsize=(15,5))

    # Ambil kolom yang ditinjau
    df = dfs[city].drop('wd', axis=1)
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Data diresample menjadi mingguan dan dihitung rata-rata dari data satu minggu
    weekly_average = df.resample('W').mean()
    

    # Loop untuk plot setiap tahun
    for year in range(start_year, end_year+1):
        # Filter data dalam tahun yang ditinjau
        filtered_df = weekly_average.loc[f'{year}-01-01':f'{year+1}-01-01']

        # Membuat garis trend polinomial
        coefficients = np.polyfit(range(len(filtered_df)), filtered_df["TEMP"], 3)
        trend_line = np.poly1d(coefficients)
        
        if year == start_year :
            # Plot pertama untuk inisialisasi label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5, label='Trend') # Plot garis trend
            ax.plot(filtered_df.index, filtered_df["TEMP"], linewidth=0.3, zorder=1, label="TEMP") # Plot linechart kolom
        else:
            # Plot tanpa label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5)  # Plot garis trend
            ax.plot(filtered_df.index, filtered_df["TEMP"], linewidth=0.3, zorder=1) # Plot linechart kolom

        plt.suptitle(f"Trend Dari Suh Udara Kota {city}")
        plt.ylabel("Suhu")
        plt.xlabel("Waktu")

    # Show plot
    plt.legend()
    return fig, ax

def rain_graph(start_year, end_year, city) :
    global dfs
    # Inisialisasi plot
    fig, ax = plt.subplots(figsize=(15,5))

    # Ambil kolom yang ditinjau
    df = dfs[city].drop('wd', axis=1)
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Data diresample menjadi mingguan dan dihitung rata-rata dari data satu minggu
    weekly_average = df.resample('W').mean()
    

    # Loop untuk plot setiap tahun
    for year in range(start_year, end_year+1):
        # Filter data dalam tahun yang ditinjau
        filtered_df = weekly_average.loc[f'{year}-01-01':f'{year+1}-01-01']

        # Membuat garis trend polinomial
        coefficients = np.polyfit(range(len(filtered_df)), filtered_df["RAIN"], 3)
        trend_line = np.poly1d(coefficients)
        
        if year == start_year :
            # Plot pertama untuk inisialisasi label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5, label='Trend') # Plot garis trend
            ax.plot(filtered_df.index, filtered_df["RAIN"], linewidth=0.3, zorder=1, label="RAIN") # Plot linechart kolom
        else:
            # Plot tanpa label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5)  # Plot garis trend
            ax.plot(filtered_df.index, filtered_df["RAIN"], linewidth=0.3, zorder=1) # Plot linechart kolom

        plt.suptitle(f"Trend Dari Intensitas Hujan Kota {city}")
        plt.ylabel("Intensitas Hujan")
        plt.xlabel("Waktu")

    # Show plot
    plt.legend()
    return fig, ax

def polutant_graph(start_year, end_year, city, polutant) :
    global dfs
    # Inisialisasi plot
    fig, ax = plt.subplots(figsize=(15,5))

    # Ambil kolom yang ditinjau
    df = dfs[city].drop('wd', axis=1)
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Data diresample menjadi mingguan dan dihitung rata-rata dari data satu minggu
    weekly_average = df.resample('W').mean()
    

    # Loop untuk plot setiap tahun
    for year in range(start_year, end_year+1):
        # Filter data dalam tahun yang ditinjau
        filtered_df = weekly_average.loc[f'{year}-01-01':f'{year+1}-01-01']

        # Membuat garis trend polinomial
        coefficients = np.polyfit(range(len(filtered_df)), filtered_df[polutant], 3)
        trend_line = np.poly1d(coefficients)
        
        if year == start_year :
            # Plot pertama untuk inisialisasi label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5, label='Trend') # Plot garis trend
            ax.plot(filtered_df.index, filtered_df[polutant], linewidth=0.3, zorder=1, label=polutant) # Plot linechart kolom
        else:
            # Plot tanpa label
            ax.plot(filtered_df.index, trend_line(range(len(filtered_df))), linestyle='--', color='red', linewidth=0.5)  # Plot garis trend
            ax.plot(filtered_df.index, filtered_df[polutant], linewidth=0.3, zorder=1) # Plot linechart kolom

        plt.suptitle(f"Trend Dari Jumlah {polutant} Kota {city}")
        plt.ylabel(f"Jumlah {polutant}")
        plt.xlabel("Waktu")

    # Show plot
    plt.legend()
    return fig, ax

with st.sidebar :
    st.subheader("Tugas Akhir Dicoding")
    st.text("raflyarj")

    selected_city = st.selectbox(
        'Pilih Kota',
        (
            'Aotizhongxin',
            'Changping',
            'Dingling',
            'Dongsi',
            'Guanyuan',
            'Gucheng',
            'Huairou',
            'Nongzhanguan',
            'Shunyi',
            'Tiantan',
            'Wanliu',
            'Wanshouxigong'
        )
    )

    start_year, end_year = st.slider(
        'Rentang Tahun',
        min_value = 2013,
        max_value = 2016,
        value=(2013, 2016)
    )

dfs = load_dataset()
st.header("Rata-Rata Suhu")

col1, col2 = st.columns(2)
mean_summer, mean_winter = count_avg_temp(start_year, end_year, selected_city)
with col1 :
    subcol1, subcol2 = st.columns([3,3])
    with subcol1 :
        st.subheader("Musim Dingin")
    with subcol2 :
        st.text("Desember - Januari")
    
    st.title(f"{round(mean_winter, 1)}°")

with col2 :
    subcol1, subcol2 = st.columns([2,2])
    with subcol1 :
        st.subheader("Musim Panas")
    with subcol2 :
        st.text("Juni - Agustus")
    
    st.title(f"{round(mean_summer, 1)}°")

st.header(f"Grafik Trend Suhu Udara Kota {selected_city}")
fig, ax = temperature_graph(start_year, end_year, selected_city)
st.pyplot(fig)

st.header(f"Grafik Trend Intensitas Hujan Kota {selected_city}")
fig, ax = rain_graph(start_year, end_year, selected_city)
st.pyplot(fig)

st.header(f"Grafik Tren Polusi Kota {selected_city}")
selected_polutant = st.selectbox(
        'Pilih Jenis Polutan',
        (
            "PM2.5",
            "PM10",
            "SO2",
            "NO2",
            "CO",
            "O3"
        )
    )
fig, ax = polutant_graph(start_year, end_year, selected_city, selected_polutant)
st.pyplot(fig)

