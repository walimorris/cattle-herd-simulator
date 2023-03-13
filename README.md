# Cattle-Herding-Simulator
A simple simulator that generates latitude/longitude data for each cattle in a herd (cattle location coming from devices that produce latitude/longitude coordinates). Simulates herding cattle due north from an initial set of coordinates and updates location coordinates every one minute in a ![Amazon DynamoDB](https://aws.amazon.com/dynamodb/) table. The DynamoDB Table is updated by devices(simulated) sending location data to a ![Amazon API Gateway](https://aws.amazon.com/api-gateway/) Endpoint via POST requests.

There are many interesting features ranchers can benefit from by using AWS during a cattle-herd movement. The first step to examining these benefits is to first simulate the movement of cattle. With a simulation you can reset, test strange cattle movements, and experiment with different useful cloud features ranchers can actually use. 

Fun facts: 
1. You may think every ranch has thousands or ten's of thousands of cattle. In some cases this is true, but according to a USDA NASS 2017 Census of Agriculture, the average size of a beef cow herd is about 44 head. ![Source](https://www.ers.usda.gov/topics/animal-products/cattle-beef/sector-at-a-glance/)

2. Cattle can generally cover 2 miles per hour. This converts to about 1 meter every second.  

More coming soon!

![cattle-herd](https://victoria.mediaplanet.com/app/uploads/sites/114/2021/05/cattle-herding.jpg)
