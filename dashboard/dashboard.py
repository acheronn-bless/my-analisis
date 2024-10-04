import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#set style seaborn
sns.set(style='dark')

# Load data
def load_data():
    data = pd.read_csv("C:/Users/Lenovo/Downloads/github/my-analisis/dashboard/days_fixed.csv")
    return data

days_df = load_data()

# Prepare for dashboard
 
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

# Menyiapkan daily rent
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily casual rent
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily registered rent
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan monthly rent
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan holiday rent
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# prepare dataframe

daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)

# Pembuatan sewa sepeda berdasarkan  musim
st.subheader('Rental based on season')

fig, ax = plt.subplots(figsize=(20, 10))

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

# jumlah penyewaan berdasarkan weekday dan holiday

st.subheader('Bike Rentals in weekday and holiday')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20,8))

colors1 = ["tab:blue", "tab:red"]
colors2 = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

#  holiday plot
sns.barplot(
  x='holiday',
  y='count',
  data=holiday_rent_df,
  palette=colors1,
  ax=axes[0])

for index, row in enumerate(holiday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Jumlah rental saat holiday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Weekday Plot
sns.barplot(
  x='weekday',
  y='count',
  data=weekday_rent_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(weekday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah rental saat weekday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Adjust layout
plt.tight_layout()

# Display the figure in Streamlit
st.pyplot(fig)


st.caption('Copyright (c) Mikhael Marcelino 2024')