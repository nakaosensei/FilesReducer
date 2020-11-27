import geopy.distance
from GPSPhoto import gpsphoto

data1 = gpsphoto.getGPSData('VID_2019_09_17_11_00_51_19_09_19_18_08_30_179.jpg')
data2 = gpsphoto.getGPSData('VID_2019_09_17_11_00_51_19_09_19_18_08_30_1838.jpg')
lat1 = (data1['Latitude'],data1['Longitude'])
lat2 = (data2['Latitude'],data2['Longitude'])
distance = geopy.distance.distance(lat1,lat2).m
print(distance)