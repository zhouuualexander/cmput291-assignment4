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
def task1(connection):
    pass
def task2(connection,Q2_count):
    number = int(input("Enter number of locations:"))
    #sql for most populous
    most = pd.read_sql_query("SELECT p.Neighbourhood_Number, p.Neighbourhood_name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_name = c.Neighbourhood_name ORDER BY p.Neighbourhood_Number DESC limit '%d' ;" %(number), connection)
    mostname = []
    for item in range(number):
        mostname.append(most.iloc[item,1])
    mostlocation = []
    for item in range(number):
        mostcoord = []
        for num in range(2,4):
            mostcoord.append(most.iloc[item,num])
        mostlocation.append(mostcoord)
    mostpopul = []
    for item in range(number):
        mostpopul.append(most.iloc[item,0])
    #sql for least populous
    least = pd.read_sql_query("SELECT p.Neighbourhood_Number, p.Neighbourhood_Name,c.Latitude,c.Longitude FROM population p,coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name ORDER BY p.Neighbourhood_Number ASC limit '%d' ;" %(number), connection)
    leastname = []
    for item in range(number):
        leastname.append(least.iloc[item,1])
    leastlocation = []
    for item in range(number):
        leastcoord = []
        for num in range(2,4):
            leastcoord.append(least.iloc[item,num])
        leastlocation.append(leastcoord)
    leastpopul = []
    for item in range(number):
        leastpopul.append(least.iloc[item,0])
    #initial the map
    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    #create most populous
    for i in range(number):
        folium.Circle(
        location=mostlocation[i], # location
        popup= mostname[i]+ " <br> " + "Population: " + str(mostpopul[i]), # popup text
        radius= 100, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m) 
    #create least populous
    for i in range(number):
        folium.Circle(
        location=leastlocation[i], # location
        popup= leastname[i]+ " <br> " + "Population: " + str(leastpopul[i]), # popup text
        radius= 100, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m) 
        m.save("Q2-" +str(Q2_count) + ".html") 
def task3(connection):
    pass
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
        for num in range(1,3):
            coord.append(crime.iloc[item,num])
        location.append(coord)
    ratio = []
    for item in range(neigh_num):
        ratio.append(crime.iloc[item,4])    
    m = folium.Map(location=[53.5444, -113.323], zoom_start=12)
    
    print(name)
    crime_type = []
    for item in name:
        for i in range(neigh_num):
            if crimetype.iloc[i,0] == item:
                crime_type.append(crimetype.iloc[i,1])
    print(crime_type)
    for i in range(neigh_num):
        folium.Circle(
        location=location[i], # location
        popup= name[i]+ " <br> " + str(ratio[i]) + " <br> " + crime_type[i], # popup text
        radius= 100, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)   
    m.save("Q4-" +str(Q4_count) + ".html")     
main()




