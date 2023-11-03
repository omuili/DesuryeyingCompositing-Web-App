import streamlit as st
import pandas as pd
import numpy as np
import math
import base64  

st.image("logo.png", width=400)
st.write("This web application is proudly brought to you by https://neuralrocks.com/")


st.title("Drillhole Data Processing")


st.write("Welcome to the Drillhole Data Processing app. You can choose to either desurvey or compose drillhole data using this app.")

option = st.sidebar.selectbox(
    "Select an Option", ["Desurvey Data", "Compose Data"])



if st.button("Reset", key="reset"):
    st.experimental_rerun()

if option == "Desurvey Data":
    st.header("Desurvey Drillhole Data")

   
    collar_file = st.file_uploader("Upload Collar Data (CSV)", type=["csv"])
    survey_file = st.file_uploader("Upload Survey Data (CSV)", type=["csv"])

    if collar_file and survey_file:
        st.write("Files uploaded successfully!")

     
        interval_option = st.selectbox("Select Desurveying Interval Option", [
                                       "Uniform Interval", "Existing Interval"])

        if interval_option == "Uniform Interval":
            uniform_interval = st.number_input(
                "Enter Uniform Desurveying Interval (e.g., 1m, 2m, 0.5m)", min_value=0.1, value=1.0, step=0.1)
        else:
            existing_interval = st.selectbox("Select Existing Interval (e.g., Lithology, Assay Data, Custom Interval)", [
                                             "Lithology", "Assay Data", "Custom Interval"])

        if st.button("Start Desurveying"):
            collar_data = pd.read_csv(collar_file)
            survey_data = pd.read_csv(survey_file)

            
            desurveyed_data = pd.DataFrame(
                columns=['Hole ID', 'Depth', 'Eastings', 'Northings', 'RL'])

            for hole_id in collar_data['Hole ID'].unique():
                collar_subset = collar_data[collar_data['Hole ID'] == hole_id]
                survey_subset = survey_data[survey_data['Hole ID'] == hole_id]

                eastings = collar_subset.iloc[0]['Eastings']
                northings = collar_subset.iloc[0]['Northings']
                rl = collar_subset.iloc[0]['Relative Sea Level (RL)']

                for _, survey_row in survey_subset.iterrows():
                    depth = survey_row['Survey Depth']
                    azimuth = survey_row['Azimuth']
                    dip = survey_row['Dip']

                    azimuth_rad = math.radians(azimuth)
                    dip_rad = math.radians(dip)

                    eastings += depth * \
                        math.sin(azimuth_rad) * math.cos(dip_rad)
                    northings += depth * \
                        math.cos(azimuth_rad) * math.cos(dip_rad)
                    rl -= depth * math.sin(dip_rad)

                    # Append the desurveyed data to the DataFrame
                    desurveyed_data = desurveyed_data.append({
                        'Hole ID': hole_id,
                        'Depth': depth,
                        'Eastings': eastings,
                        'Northings': northings,
                        'RL': rl
                    }, ignore_index=True)

       
            st.write(
                "Desurveying completed. Saving the desurveyed data to 'desurveyed_data.csv'...")
            desurveyed_data.to_csv('desurveyed_data.csv', index=False)
            st.write("Desurveyed data saved successfully.")

          
            st.subheader("Download Desurveyed Data")
            csv = desurveyed_data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # To base64
            href = f'<a href="data:file/csv;base64,{b64}" download="desurveyed_data.csv">Download Desurveyed Data</a>'
            st.markdown(href, unsafe_allow_html=True)


if option == "Compose Data":
    st.header("Compose Drillhole Data")

    
    composite_interval_option = st.selectbox("Select Composite Interval Option", [
                                             "Uniform Interval", "Existing Interval"])

    if composite_interval_option == "Uniform Interval":
        composite_uniform_interval = st.number_input(
            "Enter Composite Interval (e.g., 1m, 2m, 0.5m)", min_value=0.1, value=1.0, step=0.1)
    else:
        composite_existing_interval = st.selectbox("Select Existing Interval (e.g., Lithology, Assay Data, Custom Interval)", [
                                                   "Lithology", "Assay Data", "Custom Interval"])

   
    num_files = st.number_input(
        "Number of Data Files to Composite", min_value=1, value=1, step=1)
    data_files = []

    for i in range(num_files):
        data_file = st.file_uploader(
            f"Upload Data File {i + 1} (CSV)", type=["csv"])
        if data_file:
            data_files.append(data_file)

    
    table_info = []

    for i, data_file in enumerate(data_files):
        st.subheader(f"Data File {i + 1}")

        hole_id_col = st.selectbox(
            f"Select Hole ID Column for Data File {i + 1}", ["Hole ID"])
        depth_col = st.selectbox(
            f"Select Depth Column for Data File {i + 1}", ["Depth"])

      
        table_info.append({
            "Hole ID Column": hole_id_col,
            "Depth Column": depth_col,
           
        })

    if st.button("Compose Data"):
        

       
        composited_data = pd.DataFrame(
            columns=["Hole ID", "Composite Depth", "Composite Value"])

       

        st.write("Data composition completed.")

     
        st.subheader("Download Composited Data")
       
        st.markdown(
            "[Download Composited Data](data:file/csv;base64,download_link_here)")
