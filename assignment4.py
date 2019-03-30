import folium
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
def main():
    connection=sqlite3.connect("a4-sampled.db")
    valid = True
    Q1_count = 0
    Q2_count = 0
    Q3_count = 0
    Q4_count = 0
    while valid:
        print("1: Q1")
        print("2: Q2")
        print("3: Q3")
        print("4: Q4")
        print("E: Exit")
        task = input("Enter your choice: ")
        if task == '1':
            Q1_count = Q1_count+1
            task1(connection,Q1_count)
        elif task == '2':
            Q2_count = Q2_count+1
            task2(connection,Q2_count)
        elif task == '3':
            Q3_count = Q3_count+1
            task3(connection,Q3_count)
        elif task == '4':
            Q4_count = Q4_count +1
            task4(connection,Q4_count)
        elif task == 'E':
            valid = False
        else:
            pass
def task1(connection,Q1_count):
    start = int(input("Enter start year (YYYY):"))
    end = int(input("Enter end year (YYYY):"))
    crime = input("Enter crime type:")
        #sql = "SELECT ISNULL (SELECT Count(c.Incidents_Count) as Count,c.Month FROM crime_incidents c WHERE c.Year >= '%d' AND c.Year <='%d' AND c.Crime_Type == '%s' GROUP BY c.Month),0);" %(start,end,crime)
    sql = "SELECT Sum(c.Incidents_Count) as Count,c.Month FROM crime_incidents c WHERE c.Year >= '%d' AND c.Year <='%d' AND c.Crime_Type == '%s' GROUP BY c.Month;" %(start,end,crime)
    data = pd.read_sql_query(sql,connection)

    plot = data.plot.bar(x="Month")
    plt.plot()
    #plt.show() #pop out
    plt.savefig("Q1-"+str(Q1_count)+".png")
def task2(connection,Q2_count):
    number = int(input("Enter number of locations:"))
    #sql for most populous
<<<<<<< HEAD
    most = pd.read_sql_query("SELECT p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE, p.Neighbourhood_name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_name = c.Neighbourhood_name ORDER BY p.Neighbourhood_Number DESC limit '%d' ;" %(number), connection)
    #sql for least populous
    least = pd.read_sql_query("SELECT p.CANADIAN_CITIZEN+p.NON_CANADIAN_CITIZEN+p.NO_RESPONSE, p.Neighbourhood_Name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name ORDER BY p.Neighbourhood_Number ASC limit '%d' ;" %(number), connection)
=======
    most = pd.read_sql_query("SELECT p.Neighbourhood_Number, p.Neighbourhood_name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_name = c.Neighbourhood_name ORDER BY p.Neighbourhood_Number DESC limit '%d' ;" %(number), connection)
    #sql for least populous
    least = pd.read_sql_query("SELECT p.Neighbourhood_Number, p.Neighbourhood_Name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name ORDER BY p.Neighbourhood_Number ASC limit '%d' ;" %(number), connection)
>>>>>>> b59c911ea5bd60e295665ace5c9a11ee14c9e905
    #initial the map
    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    #create most populous
    for i in range(number):
        folium.Circle(
        location=[most.iloc[i,2],most.iloc[i,3]], # location
        popup= most.iloc[i,1] + " <br> " + "Population: " + str(most.iloc[i,0]), # popup text
        radius= int(most.iloc[i,0])/10, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)

    for i in range(number):
        folium.Circle(
        location=[least.iloc[i,2],least.iloc[i,3]], # location
        popup= least.iloc[i,1] + " <br> " + "Population: " + str(least.iloc[i,0]), # popup text
        radius= int(least.iloc[i,0])/10, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)
    m.save("Q2_" +str(Q2_count) + ".html")


def task3(connection,Q3_count):
    start = int(input("Enter start year (YYYY):"))
    end = int(input("Enter end year (YYYY):"))
    crime = str(input("Enter crime type:"))
    num = int(input("Enther number of neighborhoods:"))
    sql = "SELECT ci.Neighbourhood_Name,cd.Latitude,cd.Longitude,SUM(ci.Incidents_Count) as total FROM crime_incidents ci, coordinates cd WHERE ci.Neighbourhood_Name = cd.Neighbourhood_Name \
    AND ci.Year >= '%d' AND ci.year <='%d' AND ci.crime_type='%s' GROUP BY ci.Neighbourhood_Name ORDER BY total DESC limit '%d'; " %(start,end,crime,num)
    nb = pd.read_sql_query(sql,connection)

    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    for i in range(num):
        folium.Circle(
        location= [nb.iloc[i,1],nb.iloc[i,2]],
        popup = nb.iloc[i,0] + "<br>" + str(nb.iloc[i,3]),
        radius = int(nb.iloc[i,3]),
        color = "crimson",
        fill= True,
        fill_color= 'crimson').add_to(m)
    m.save("Q3_"+str(Q3_count)+".html")



def task4(connection,Q4_count):
    lower_year = int(input("Enter start year (YYYY):"))
    upper_year = int(input("Enter end year (YYYY):"))
    neigh_num = int(input("Enter number of neighborhoods:"))
    crime = pd.read_sql_query("select Neighbourhood_Name,Latitude,Longitude,Crime_Type,ratio,SUM(Incidents_Count) from (SELECT r.Neighbourhood_Name,c.Latitude,c.Longitude,r.Crime_Type,(SUM(r.Incidents_Count)/CAST(p.Neighbourhood_Number AS float))as ratio,r.Incidents_Count\
    FROM population p,coordinates c ,crime_incidents r WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND p.Neighbourhood_Name = r.Neighbourhood_Name\
    AND r.year>= '%d' AND r.year<='%d' GROUP BY r.Neighbourhood_Name ORDER BY ratio DESC limit '%d') group by Neighbourhood_Name ORDER BY ratio DESC;" %((lower_year),(upper_year),(neigh_num)), connection)
    #print(crime)
    neigh_name = crime['Neighbourhood_Name']
    neigh_name.to_sql("Names",connection,if_exists='replace')
    crimetype = pd.read_sql_query("SELECT temp.Neighbourhood_Name,temp.Crime_Type,MAX(temp.summer) FROM (SELECT r.Neighbourhood_Name,r.Crime_Type,SUM(r.Incidents_Count) as summer FROM Names n ,crime_incidents r WHERE r.Neighbourhood_Name = n.Neighbourhood_Name and r.year>= '%d' AND r.year<='%d'Group by r.Neighbourhood_Name,r.Crime_Type)temp  Group by temp.Neighbourhood_Name ;" %((lower_year),(upper_year)) , connection)
    name = []
    for item in range(neigh_num):
        name.append(crime.iloc[item,0])
    location = []
    for item in range(neigh_num):
        coord = []
        for num in range    (1,3):
            coord.append(crime.iloc[item,num])
        location.append(coord)
    ratio = []
    for item in range(neigh_num):
        ratio.append(crime.iloc[item,4])
    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    crime_type = []
    for item in name:
        for i in range(neigh_num):
            if crimetype.iloc[i,0] == item:
                crime_type.append(crimetype.iloc[i,1])
    for i in range(neigh_num):
        folium.Circle(
        location=location[i], # location
        popup= name[i]+ " <br> " + str(ratio[i]) + " <br> " + crime_type[i], # popup text
        radius= (crime.iloc[i,4])*1000, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)
    m.save("Q4-" +str(Q4_count) + ".html")
main()
