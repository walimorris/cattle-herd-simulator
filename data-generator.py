import boto3 
import random
import math
import time

from decimal import Decimal

"""
Given the earth's radius value we can calculate the latitude and 
longitude offset in meters.

cLat - the current latitude value
cLong - the current longitude value
oLat - latitude offset in meters
oLong - longitude offset in meters

returns an array given the offset latitude and longitude [lat, long]
"""
def offset(cLat, cLong, oLat, oLong): 
    
    # Earth's radius - sphere
    R = 6378137
    
    # Coordinate's offset in radian
    dLat = oLat/R
    dLong = oLong/(R*math.cos(math.pi*cLat/180))
    
    f_lat = round(cLat + dLat * 180/math.pi, 6)
    f_long = round(cLong + dLong * 180/math.pi, 6)
    
    coordinates = [f_lat, f_long]
    
    return coordinates
    
"""
Given the total number of cattle head (cattle in herd), generate an id 
for each cattle head given the low bound, high bound and fixed number 
of digits in a id. 

return an array of ids 
"""
def generateCattleIds(num_cattle_head, low, high, fixed_digits):
    # generate cattle ids
    cattle_ids = []
    for i in range(num_cattle_head):
        id_gen = random.randrange(low, high, fixed_digits)
        cattle_ids.append(id_gen)
        
    return cattle_ids    
    
"""
Generate initial latitude/longitude location data per cattle id. An id 
represents a device worn by a single cattle. The way coordinates are 
generated responds best to a total number of ids that are divisible by 5.
In this way we can offset coordinates by a meter. 

returns a dict (map) that models a device id -> and array containing the 
initial [lat, long] coordinates for each device. 

example: deviceid -> [47.963996, -122.162001]
"""
def initalizeDeviceLocationData(cattle_ids):
    x = 0 
    y = 0
    cattle_map = {}

    # generate initial location data for each device in the herd
    # a device is known by the 'cattle_id' each cattle with a device
    for i in range(len(cattle_ids)):
        coords = offset(47.963996, -122.162001, x, y)
        cattle_map[cattle_ids[i]] = coords
        y = y + 1
        if (y == 5):
            y = 0
            x = x + 1
    
    return cattle_map   
    
"""
Cow can cover 2 miles per hour. This converts to about 1 meter every second. 
So this converts to 60 meters in 1 minute or 10 meters in 10 seconds and so 
on. This method herds each cattle north 1m. 
"""
def herdCattleNorthOneMeter(cattle_map):
    new_cattle_map = {}
    for cattle_id in cattle_map:
        currentValues = cattle_map[cattle_id]
        coords = offset(currentValues[0], currentValues[1], 1, 0)
        new_cattle_map[cattle_id] = coords
        
    return new_cattle_map    
    
"""
Simulate hearding a group of x cattle for one minute. Every 1 second simulates 
each cattle moving 1m per sec. For 60 secs / 60 meters get the new coordinates 
of each cattle in the cattle map which should represent each cattle 60 meters
north of the original coordinates.
"""
def herdCattleForOneMinute(cattle_map):
    new_cattle_map = cattle_map
    for i in range(60): 
        #pause 1 sec 
        time.sleep(1)
        new_cattle_map = herdCattleNorthOneMeter(new_cattle_map)
        
    return new_cattle_map    

"""
Simulates herding a group of cattle for one hour. With the given algorithms and 
functions. Know that cattle move 1m every 1 sec. In this case, simulate a herd 
of cattle moving north and updating a dynamodb table's latitude/longitude data 
attributes every one minutes. Latitude/Longitude values will change every one 
minute, with a 60 meter north/south offset.
"""
def herdCattleForOneHour(herding_table, cattle_map):
    for i in range(60):
        # After initial location generation, there should be x number of devices with 
        # latitude and longitude data populated in the dynamodb table. Now we should 
        # create a process to update location data every x minutes and update each 
        # device location data in the dynamodb table
        cattle_map = herdCattleForOneMinute(cattle_map)
        updateDeviceLocationData(herding_table, cattle_map)
        print("Location data updated!")
        
        
    
"""
Populate the dynamodb herding table with initial location data for each device
with a deviceid, latitude attribute and longitude attribute. 

Iterate through the cattle_map. Each key represents a deviceid and maps to an 
array that contains two values: [latitude, longitude]
"""
def populateInitialLocationData(cattle_map, herding_table):
    # add each device with location to table 
    for cattle_id in cattle_map:
        values = cattle_map[cattle_id]
        herding_table.put_item(
            Item = {
                'deviceid': cattle_id,
                'latitude': str(values[0]),
                'longitude': str(values[1])
            }
        )
 
"""
Update device data in the dynamodb herding table given the deviceid, 
new latitude and longitude value.
"""
def updateDeviceLocationData(herding_table, cattle_map):
    for cattle_id in cattle_map:
        locationValues = cattle_map[cattle_id]
        
        herding_table.update_item(
            Key = {
                'deviceid': cattle_id
            },
            UpdateExpression = 'SET latitude=:latitude, longitude=:longitude',
            ExpressionAttributeValues = {
                ':latitude': str(locationValues[0]),
                ':longitude': str(locationValues[1])
            }
        )
    
    
dynamodb = boto3.resource('dynamodb')
num_cattle_head = 50
fixed_digits = 6
low_range = 111111
high_range = 999999

# dynamodb herding table
herding_table = dynamodb.Table('your-table-name')

# generate ids for each cattle head 
cattle_ids = generateCattleIds(num_cattle_head, low_range, high_range, fixed_digits)

# generate dictionary 
cattle_map = initalizeDeviceLocationData(cattle_ids)

populateInitialLocationData(cattle_map, herding_table)
print("Initial Herd data uploaded!")

herdCattleForOneHour(herding_table, cattle_map)
