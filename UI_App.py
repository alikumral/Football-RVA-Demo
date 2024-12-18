import streamlit as st
import pandas as pd
import altair as alt

# Load the datasetpip
df = pd.read_csv('final_predictions_by_position.csv', encoding='ISO-8859-1')
df['Name'] = df['Name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ISO-8859-1')

# App title
st.title("Football Player Analysis")

# Sidebar filters
st.sidebar.header("Filter Options")

# Filter by position
position = st.sidebar.multiselect("Position", options=df["Position_Cluster_fifa"].unique())

# Filter by club
club = st.sidebar.multiselect("Club", options=df["Club_fifa"].unique())

# Filter by age range
age_range = st.sidebar.slider("Age Range", int(df["Age_fifa"].min()), int(df["Age_fifa"].max()), (int(df["Age_fifa"].min()), int(df["Age_fifa"].max())))

# Filter by market value
market_value_range = st.sidebar.slider("Market Value Range", float(0.1), float(df["market_value_in_eur"].max()), (float(0.1), float(df["market_value_in_eur"].max())))

# Apply filters
filtered_df = df.copy()

if position:
    filtered_df = filtered_df[filtered_df["Position_Cluster_fifa"].isin(position)]

if club:
    filtered_df = filtered_df[filtered_df["Club_fifa"].isin(club)]

filtered_df = filtered_df[(filtered_df["Age_fifa"] >= age_range[0]) & (filtered_df["Age_fifa"] <= age_range[1])]
filtered_df = filtered_df[(filtered_df["market_value_in_eur"] >= market_value_range[0]) & (filtered_df["market_value_in_eur"] <= market_value_range[1])]

# Display filtered data count
st.header("Filtered Player Database")
st.write(f"Total Players Found: {len(filtered_df)}")

# Option to select specific columns to display
st.sidebar.header("Select Columns to Display")
columns_to_display = st.sidebar.multiselect("Columns", options=df.columns.tolist(), default=df.columns.tolist())

# Display the selected columns with Euro sign
if columns_to_display:
    display_df = filtered_df[columns_to_display].copy()

    # Apply Euro sign formatting to relevant columns
    if 'market_value_in_eur' in display_df.columns:
        display_df['market_value_in_eur'] = display_df['market_value_in_eur'].apply(lambda x: f"€{x:,.2f}")
    if 'predicted_market_value' in display_df.columns:
        display_df['predicted_market_value'] = display_df['predicted_market_value'].apply(lambda x: f"€{x:,.2f}")

    # Display the DataFrame with formatted values
    st.dataframe(display_df)

# Add a section to display visualizations
st.header("Visualizations")

# Define the desired color
desired_color = '#90ff02'

# Distribution of Market Value by Position
st.subheader("Market Value Distribution by Position")

# Prepare data
market_value_data = filtered_df.groupby("Position_Cluster_fifa")["market_value_in_eur"].mean().reset_index()

# Create Altair chart
market_value_chart = alt.Chart(market_value_data).mark_bar().encode(
    x=alt.X('Position_Cluster_fifa:N', title='Position'),
    y=alt.Y('market_value_in_eur:Q', title='Average Market Value (€)'),
    tooltip=['Position_Cluster_fifa', 'market_value_in_eur'],
    color=alt.value(desired_color)  # Set the bar color
).properties(
    width=600,
    height=400
)

st.altair_chart(market_value_chart, use_container_width=True)

# Average Age by Club
st.subheader("Average Age by Club")

# Prepare data
average_age_data = filtered_df.groupby("Club_fifa")["Age_fifa"].mean().reset_index()

# Create Altair chart
average_age_chart = alt.Chart(average_age_data).mark_bar().encode(
    x=alt.X('Club_fifa:N', title='Club', sort='-y'),
    y=alt.Y('Age_fifa:Q', title='Average Age'),
    tooltip=['Club_fifa', 'Age_fifa'],
    color=alt.value(desired_color)  # Set the bar color
).properties(
    width=600,
    height=400
).configure_axis(
    labelAngle=-45  # Rotate x-axis labels if needed
)

st.altair_chart(average_age_chart, use_container_width=True)

# Distribution of Player Ages
st.subheader("Distribution of Player Ages")

# Prepare data
age_distribution_data = filtered_df["Age_fifa"].value_counts().reset_index()
age_distribution_data.columns = ['Age', 'Count']

# Create Altair chart
age_distribution_chart = alt.Chart(age_distribution_data).mark_bar().encode(
    x=alt.X('Age:O', title='Age', sort='ascending'),
    y=alt.Y('Count:Q', title='Number of Players'),
    tooltip=['Age', 'Count'],
    color=alt.value(desired_color)  # Set the bar color
).properties(
    width=600,
    height=400
)

st.altair_chart(age_distribution_chart, use_container_width=True)

# Save the filtered data to a CSV file
st.sidebar.header("Download Options")
if st.sidebar.button("Download Filtered Data as CSV"):
    filtered_df.to_csv("filtered_players.csv", index=False)
    st.sidebar.success("CSV file has been generated!")

st.sidebar.header("About")
st.sidebar.text("This app allows you to filter \nand explore football player data.")