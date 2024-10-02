import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/data_baru.csv')
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)
    return data

data = load_data()

# Sidebar for user input
st.sidebar.header('User Input Features')
selected_station = st.sidebar.selectbox('Select Station', data['station'].unique())

# Main page
st.title('Air Quality Dashboard')

# Question 1: Factors influencing PM2.5 levels
st.header('Factors Influencing PM2.5 Levels')

# Calculate correlations
corr = data.select_dtypes(include=[np.number]).corr()
top_corr = corr['PM2.5'].abs().sort_values(ascending=False).iloc[1:6]

st.write("Top 5 features correlated with PM2.5:")
st.write(top_corr)

# Scatter plot
feature = st.selectbox('Select feature to plot against PM2.5', top_corr.index)
fig, ax = plt.subplots()
sns.scatterplot(data=data[data['station'] == selected_station], x=feature, y='PM2.5')
st.pyplot(fig)

# Question 2: Seasonal patterns
st.header('Seasonal Patterns of Air Quality')

data['month'] = data.index.month
data['season'] = data['month'].map({12:'Winter', 1:'Winter', 2:'Winter',
                                    3:'Spring', 4:'Spring', 5:'Spring',
                                    6:'Summer', 7:'Summer', 8:'Summer',
                                    9:'Autumn', 10:'Autumn', 11:'Autumn'})

fig, ax = plt.subplots()
sns.boxplot(data=data[data['station'] == selected_station], x='season', y='PM2.5')
st.pyplot(fig)

# Question 3: Relationship between meteorological conditions and pollutants
st.header('Relationship between Meteorological Conditions and Pollutants')

variables = ['PM2.5', 'TEMP', 'WSPM', 'RAIN', 'SO2', 'NO2', 'CO', 'O3']
correlation_matrix = data[variables].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Question 4: Stations with poorest air quality
st.header('Stations with Poorest Air Quality')

avg_pm25 = data.groupby('station')['PM2.5'].mean().reset_index()

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='station', y='PM2.5', data=avg_pm25, hue='station', ax=ax)
plt.title('Average PM2.5 Levels by Station')
plt.xlabel('Station')
plt.ylabel('Average PM2.5')
plt.xticks(rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)

st.write("Recommendations for improvement:")
st.write("1. Implement stricter emission controls in areas with consistently high PM2.5 levels.")
st.write("2. Increase green spaces and tree planting initiatives to help filter air pollutants.")
st.write("3. Promote the use of public transportation and clean energy vehicles to reduce traffic-related emissions.")
st.write("4. Enhance monitoring and enforcement of industrial emissions standards.")