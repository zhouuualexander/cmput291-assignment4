import folium
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
def main():
    connection=sqlite3.connect("a4-sampled.db")
    valid = True
    Q2_count = 0
    Q4_count = 0
    while valid:
        print("1: Q1")
        print("2: Q2")
        print("3: Q3")
        print("4: Q4")
        print("E: Exit")
        
        task = input("Enter your choice: ")
        if task == '1':
            task1(connection)
        elif task == '2':
            Q2_count = Q2_count+1
            task2(connection,Q2_count)
        elif task == '3':
            task3(connection)
        elif task == '4':
            Q4_count = Q4_count +1
            task4(connection,Q4_count)
        elif task == 'E':
            valid = False
        else:
            pass
def task1(connection):
    paper = pd.read_sql_query("select * from papers;",connection)
    count = len(paper.index)
    browsing = True
    paper_id = int(respond)-1
    print("You selected paper " + respond + " which is " + paper["title"][paper_id])
    print("The email of all reviewers that have reviewed the paper is below")
    sql = "SELECT r.reviewer FROM papers p, reviews r WHERE p.Id = r.paper AND p.Id = '%s';" % (respond)
    reviewer = pd.read_sql_query(sql,connection)
    print(reviewer)
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
    crime = pd.read_sql_query("SELECT  p.Neighbourhood_Name,c.Latitude,c.Longitude,r.Crime_Type,(SUM(r.Incidents_Count)/CAST(p.Neighbourhood_Number AS float))as ratio\
    FROM population p,coordinates c ,crime_incidents r WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND p.Neighbourhood_Name = r.Neighbourhood_Name\
    AND r.year>= '%d' AND r.year<='%d' GROUP BY r.Neighbourhood_Name ORDER BY ratio DESC limit '%d';" %((lower_year),(upper_year),(neigh_num)), connection)
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
    for i in range(neigh_num):
        folium.Circle(
        location=location[i], # location
        popup= name[i]+ " <br> " + str(ratio[i]), # popup text
        radius= 100, # size of radius in meter
        color= 'crimson', # color of the radius
        fill= True, # whether to fill the map
        fill_color= 'crimson' # color to fill with
        ).add_to(m)   
    m.save("Q4-" +str(Q4_count) + ".html") 
    print(ratio)
    print(name)
    print(location)
    print(crime)
main()


