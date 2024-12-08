import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set Seaborn visualization theme
sns.set_theme(style="whitegrid")

# Read data from CSV file
main_df = pd.read_csv("dashboard/main_data.csv")

# Add logo or image to sidebar
st.sidebar.image("dashboard/bike.jpg", use_column_width=True)

# Sidebar for filtering date range
st.sidebar.header("Filter Date Range")
start_date = st.sidebar.date_input("Select Start Date", pd.to_datetime(main_df['dteday'].min()))
end_date = st.sidebar.date_input("Select End Date", pd.to_datetime(main_df['dteday'].max()))

# Filter data based on selected date range
filtered_df = main_df[(main_df['dteday'] >= str(start_date)) & (main_df['dteday'] <= str(end_date))]

# Dashboard Title
st.title("🚴‍♂️ Bike Rental Dashboard 🚴‍♀️")
st.write("""Welcome to the **Bike Rental Dashboard**! 
Discover interesting insights from bike rental data through interactive visualizations.""")

# 1. Monthly Bike Usage Trend
st.header("📅 Monthly Bike Usage Trend")
monthly_trend = filtered_df.groupby(['year', 'month'], observed=True)['count'].sum().reset_index()

# Ensure the 'year' column is of integer type
monthly_trend['year'] = monthly_trend['year'].astype(int)

# Set the order of months
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=months_order, ordered=True)

# Create visualization
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x='month', y='count', hue='year', marker='o', palette='tab10', ax=ax)
ax.set_title('Monthly Bike Usage Trend', fontsize=16)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Rentals', fontsize=12)
ax.legend(title='Year', loc='upper right')
st.pyplot(fig)

# Display data table
st.subheader("Monthly Trend Table")
st.dataframe(monthly_trend)

# 2. Weather Influence on Bike Usage
st.header("🌤️ Weather Influence on Bike Usage")
weather_rentals = filtered_df.groupby('weather_situation', observed=True)['count'].agg(['sum', 'mean']).reset_index()

# Visualize the effect of weather
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_rentals, x='weather_situation', y='sum', palette='coolwarm', ax=ax)
ax.set_title('Weather Influence on Bike Rentals', fontsize=16)
ax.set_xlabel('Weather Condition', fontsize=12)
ax.set_ylabel('Total Rentals', fontsize=12)
st.pyplot(fig)

# Display data table
st.subheader("Weather Influence Table")
st.dataframe(weather_rentals)

# 3. Bike Rentals by Day Type
st.header("📊 Bike Rentals by Day Type")
filtered_df['day_type'] = filtered_df['weekday'].apply(lambda x: 'Weekend' if x in ['Sat', 'Sun'] else 'Weekday')
day_type_rentals = filtered_df.groupby('day_type')['count'].mean().reset_index()

# Visualize day type rentals
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=day_type_rentals, x='day_type', y='count', palette='muted', ax=ax)
ax.set_title('Bike Rentals by Day Type', fontsize=16)
ax.set_xlabel('Day Type', fontsize=12)
ax.set_ylabel('Average Rentals', fontsize=12)
st.pyplot(fig)

# Display data table
st.subheader("Day Type Rentals Table")
st.dataframe(day_type_rentals)

# 4. Bike Rental Proportion
st.header("👥 Bike Rental Proportion")
user_type_counts = filtered_df[['casual', 'registered']].sum()

# Create pie chart visualization
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(user_type_counts, labels=['Casual', 'Registered'], autopct='%1.1f%%', startangle=90, colors=['#8fbc8f', '#d87093'])
ax.set_title('Bike Rental Proportion', fontsize=16)
st.pyplot(fig)

# Display data table
st.subheader("User Proportion Table")
st.dataframe(user_type_counts.reset_index(name='Total'))

# Closing Message
st.sidebar.markdown("### 🌟 Thank you for using the Bike Rental Dashboard!")
st.caption("Copyright © Syaripatul Aini 2024")
