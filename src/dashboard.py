import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from ydata_profiling import ProfileReport
import dbUtills
import seaborn as sns
import traceback

try:
         # Generate report
        #traffic_violationDF = dbUtills.fetch_data("SELECt * FROM traffic_violation")
        #profile = ProfileReport(traffic_violationDF, title="EDA Report", explorative=True)
        # Save report
        #profile.to_file("Traffic_ViolationEDA_Report.html")

    # ---------------- SIDEBAR ---------------- #
        traffic_violationDF = dbUtills.fetch_data("SELECt * FROM traffic_violation")

        st.sidebar.title("Analytical Views")
        option = st.sidebar.radio(
            "Navigate",
            ("Home","Heatmaps","Search & Filtering")
        )
        if option =="Home":
            st.title("Traffic Violations Insight Dashboard")
    
             # Show Trafic violation by type
            st.header("Violation Types", divider="gray")
            fig =  dbUtills.top10ViolationType(traffic_violationDF)
            st.pyplot(fig)

        #show state wise violation
            st.header("Traffic Violation distribution by State", divider="gray")
            fig1= dbUtills.trafficViolationByState(traffic_violationDF)
            st.pyplot(fig1)

        #show Vehilce maker'ss wise violation
            st.header("Traffic Violation distribution by vehicle Makers", divider="gray")
            fig2= dbUtills.traffic_violation_ByMake(traffic_violationDF)
            st.pyplot(fig2)
    

        #show geolocation wise  violation
            st.header("Traffic Violation distribution by Geolocation", divider="gray")
            fig3= dbUtills.trafficViolationByGeolocation(traffic_violationDF)
            st.pyplot(fig3)
        #Gender Distribution within Each Race
            st.header("Traffic Violation by Gender Distribution within Each Race", divider="gray")
            fig4 = dbUtills.ViolationByRaceAndGender(traffic_violationDF)
            st.pyplot(fig4)

            fig5 = dbUtills.trafficViolationByYear(traffic_violationDF)
            st.pyplot(fig5)
        
        if option == "Heatmaps":
              # Heatmap 
            st.header("Heatmap",divider="gray")
            fig_violationHeatmap, ax = plt.subplots(figsize =(10,8))
            sns.heatmap(traffic_violationDF.select_dtypes(include="number").corr(), annot=True,cmap="coolwarm") 
            st.pyplot(fig_violationHeatmap)

            #Gender and Violation Column Heatmap
            cross_tab = pd.crosstab(
                traffic_violationDF["Gender"],
                traffic_violationDF["Violation_Type"]
                )

            figHeatmap = plt.figure(figsize=(12,5))
            sns.heatmap(cross_tab, annot=True, fmt="d")
            st.header("Gender vs Violation Type Heatmap")
            st.pyplot(figHeatmap)
    
        # Search and Filter 
        if option == "Search & Filtering":
            st.title("Search & Filtering Traffic Violations")
  
            location = st.sidebar.selectbox("Select location ", traffic_violationDF["Location"].drop_duplicates(),index=None)
            vehicle_type = st.sidebar.selectbox("Select Vehicle Type ",traffic_violationDF["VehicleType"].drop_duplicates(),index= None)
            gender = st.sidebar.selectbox("Select gender ", traffic_violationDF["Gender"].drop_duplicates(),index= None)
            race = st.sidebar.selectbox("Select race ", traffic_violationDF["Race"].drop_duplicates(),index= None)
            violation_category = st.sidebar.selectbox("Violation_Category", traffic_violationDF["Violation_Type"].drop_duplicates(),index= None)
   
   
            if st.sidebar.button("Submit", type="primary"):
           
             # filter based on Location
                filtered_df = traffic_violationDF.copy()

                mask = pd.Series(True, index=filtered_df.index)

                if location:
                    mask &= filtered_df["Location"].eq(location)

                if vehicle_type:
                    mask &= filtered_df["VehicleType"].eq(vehicle_type)

                if gender:
                    mask &= filtered_df["Gender"].eq(gender)

                if race:
                    mask &= filtered_df["Race"].eq(race)

                if violation_category:
                    mask &= filtered_df["Violation_Type"].eq(violation_category)

                filtered_df = filtered_df.loc[mask]
        
                st.subheader("Filtered Traffic Violations")
                 # convert all tinyint type into True and False

                boolType_cols= ["Accident","Belts", "Personal_Injury", "Property_Damage", "Fatal", 
                    "Commercial_License", "HAZMAT", "Commercial_Vehicle", "Alcohol","Work_Zone","Search_Conducted","Contributed_To_Accident"]
      
                filtered_df[boolType_cols] = (filtered_df[boolType_cols].astype(bool).astype(str))
                # filtered_df["Contributed_To_Accident"]= (filtered_df["Contributed_To_Accident"].map({0 : False, 1 : True})).astype(str)
                # filtered_df["Time_Of_Stop"] = pd.to_datetime(filtered_df["Time_Of_Stop"].dt.strftime("%H:%M:%S"))      
                filtered_df["Time_Of_Stop"] = (pd.Timestamp("1900-01-01")+filtered_df["Time_Of_Stop"]).dt.time
                st.dataframe(filtered_df)
except Exception as e:
        st.exception(e)
        st.code(traceback.format_exc())

