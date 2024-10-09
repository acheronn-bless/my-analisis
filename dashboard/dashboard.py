import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/acheronn-bless/my-analisis/refs/heads/main/dashboard/dayy.csv")
    return data

# Fungsi untuk memperbarui label dari numerik ke kategorikal
def update_labels(df):
    # Ubah kolom 'holiday' dari angka 0 dan 1 menjadi 'Tidak' dan 'Ya'
    df['holiday'] = df['holiday'].map({0: 'Tidak', 1: 'Ya'})
    
    # Ubah kolom 'weekday' dari angka (0-6) menjadi nama hari
    df['weekday'] = df['weekday'].replace({
        0: 'Senin', 
        1: 'Selasa', 
        2: 'Rabu', 
        3: 'Kamis', 
        4: 'Jumat', 
        5: 'Sabtu', 
        6: 'Minggu'
    })
    
    # Ubah kolom 'season' dari angka menjadi label kategorikal
    df['season'] = df['season'].replace({
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'
    })
    
    return df

# Load data dan perbarui label
days_df = load_data()
days_df = update_labels(days_df)

# Judul dashboard
st.title('Sewa Sepeda Dashboard')

# Filter component
min_date = pd.to_datetime(days_df['date']).dt.date.min()
max_date = pd.to_datetime(days_df['date']).dt.date.max()

start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = days_df[(days_df['date'] >= str(start_date)) & 
                (days_df['date'] <= str(end_date))]

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Plot untuk penyewaan berdasarkan musim
st.subheader('Rental based on season')
season_rent_df = create_season_rent_df(main_df)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:red',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:blue',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Menambahkan subjudul untuk 'Jumlah penyewaan berdasarkan weekday dan holiday'
st.subheader('Bike Rentals in weekday and holiday')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 12))

colors1 = ["tab:blue", "tab:red"]
colors2 = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

# Mengurutkan kategori pada kolom 'weekday'
order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
main_df['weekday'] = pd.Categorical(main_df['weekday'], categories=order, ordered=True)

# Plot untuk holiday
holiday_rent_df = main_df.groupby('holiday').agg({'count': 'sum'}).reset_index()
sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=colors1,
    ax=axes[0]
)

for index, row in enumerate(holiday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Jumlah rental saat holiday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Plot untuk weekday
weekday_rent_df = main_df.groupby('weekday').agg({'count': 'sum'}).reset_index()
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors2,
    ax=axes[1]
)

for index, row in enumerate(weekday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah rental saat weekday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Adjust layout to fit both subplots well
plt.tight_layout()

# Display the figure in Streamlit
st.pyplot(fig)

st.caption('Copyright (c) Mikhael Marcelino 2024')