import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------- DB CONNECTION ---------------- #
def get_connection():  
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sql@1234",
        database="traffic_violationsdb"
    )

# function to fecth data from database   
def fetch_data(query, params=None):
    try:
       # get Sql Connection
        conn = get_connection()
       # get cursor
        cursor = conn.cursor()

        #excute querry 
        cursor.execute(query, params)

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        df = pd.DataFrame(rows, columns=columns)

        cursor.close()
        conn.close()
        return df
    finally:
        if conn:
            conn.close()

#Graphes 
def top10ViolationType(df):
    fig,ax = plt.subplots(figsize =(10,5))
    top_violation = (df["Violation_Type"].value_counts().head(10))
    
    #ax.set_title("Number of Traffic Violations by Violation_Type")
    ax.pie(top_violation.values,labels=top_violation.index,autopct='%1.1f%%')
    #plt.bar(top_violation.index,top_violation.values)
    #plt.xlabel("Violation Type")
    #plt.ylabel("Count")
    #plt.xticks(rotation=45)
    return fig


def trafficViolationByState(df):
    fig,ax = plt.subplots(figsize =(10,5))
    top_violation = (df["State"].value_counts().head(10))
    
   #ax.set_title("Traffic Violations distribution by State")
    plt.bar(top_violation.index,top_violation.values)
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    return fig

def trafficViolationByGeolocation(df):
    fig,ax = plt.subplots(figsize =(10,5))
    top_violation = (df["Geolocation"].value_counts().head(10))
    #ax.set_title("Traffic Violations distribution by Geolocation")
    plt.bar(top_violation.index,top_violation.values)
    plt.xlabel("Geolocation")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    return fig


def ViolationByRaceAndGender(df):
    race_gender_pct = pd.crosstab(
        df["Race"],
        df["Gender"],
        normalize="index"
         ) * 100
    
    ax = race_gender_pct.plot(
        kind="bar",
        stacked=True,
        figsize=(12, 6)
        )
    #ax.set_title("Traffic Violations by Gender Distribution within Each Race")
    ax.set_xlabel("Race")
    ax.set_ylabel("Percentage")
    ax.legend(title="Gender")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax.get_figure()

#Traffic Violations distribution by Makes
def traffic_violation_ByMake(df):
    fig,ax = plt.subplots(figsize =(6,6))
    top_violation = (df["Make"].value_counts().head(10))
    ax.pie(top_violation.values,labels=top_violation.index,autopct='%1.1f%%' )
    return fig

def trafficViolationByYear(df):
    
     #Convert order_date to datetime
     yearly_counts = df.groupby("Year").size().reset_index(name="Count")
    # Count shipments per month
    
     fig, ax = plt.subplots(figsize=(10, 5))

     ax.plot(
          yearly_counts["Year"],
          yearly_counts["Count"],
          marker="o"
     )
        
     ax.set_title("Yearly Traffic Violation Trends")

     ax.set_xlabel("Year")
     ax.set_ylabel("Number of Traffic_Violations")
     ax.grid(True)
 
     plt.xticks(rotation=45)
     plt.tight_layout()
     return fig
 



    



