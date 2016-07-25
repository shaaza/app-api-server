FORMAT: 1A

# Energy Data
Energy Data is an internal API Gateway used for energy data access, updation, processing and visualization by Engazeapp, and also for other internal services.

# Energy Data API Root [/]
This resource does not have any attributes.

## Retrieve the Entry Point [GET]

+ RESPONSE 200 (application/json)

        {
            "app_url": "/app",
            "datalab_url": "/datalab",
            "crons_url": "/crons"
        }


## GROUP App

### GROUP Data
-------------------------------

### Suggested Activities [/app/data/activities/{language}/{instance_no}/{goals}]
---
A Suggested Activities object has the following attributes:

+ activities: An array of Activity objects, selected based on parameters.

+ Parameters
	+ language (required, {en,da}) - language of content of activity objects
	+ instance_no (required, number) - instance number of the consumer accessing app
	+ goal (required, string) - string of 3 comma-separated 0/1 values indicating goal selection

#### View the activities [GET]

+ Response 200 (application/json)

		+ Body
			{
			  "activities": [
			    {
			      "activity_active_hours": 3, 
			      "activity_frequency": 0.4, 
			      "appliance_specific": 0, 
			      "co2Change": -0.5178780000000001, 
			      "dependency_parameters": [ ... ], 
			      "id": 1, 
			      "image": "1.png", 
			      "impact_points_change": 0, 
			      "interval_specific": 1, 
			      "kwh_per_cycle": 0, 
			      "localChange": 0, 
			      "moneyChange": -2.5920000000000005, 
			      "num_sms_per_day_per_action": 1, 
			      "pledge": { ... }, 
			      "pledge_active_hours": 2, 
			      "special_days": 0, 
			      "tags": [ ... ], 
			      "text": "Messages to make your mornings energy efficient.", 
			      "title": "Mornings", 
			      "user_data_dependent": 1
			    },
			    {...}, {...}, {...}, {...}, {...} 
			  ]
			} 


### GROUP Graphs
-------------------------------


### Goal Graph Data [/app/graphs/selectGoal/{instance_no}
---
Data for the graphs of the Select Goal stage of onboarding module.

+ graphData: An object consisting of data objects for different graphs
	+ co2GraphData: An object consisting of a data array and a settings object.
	+ localGraphData: An object consisting of a value, benchmark and title.
	+ moneyGraphData: An object consisting of a data array and a settings object.

+ Parameters
	+ instance_no (required, number) - instance number of the consumer accessing app

#### Get the graph data [GET]

+ Response 200 (application/json)

		+ Body
			{
			  "graphData": {
			    "co2GraphData": {
			      "data": [ { ... }, { ... } ], 
			      "settings": { ...  }
			    }, 
			    "localGraphData": { "benchmark": 35, "title": "null", "value": 45 }, 
			    "moneyGraphData": {
			      "data": [ { ... }, { ... } ], 
			      "settings": { ...  }
			    }
			  }
			}



### Activities Graph Data [/app/graphs/selectActivities/{instance_no}
---
Data for the graphs of the Select Activities stage of onboarding module.

+ graphData: An object consisting of data objects for different graphs
	+ co2GraphData: An object consisting of a data array and a settings object.
	+ localGraphData: An object consisting of a value, benchmark and title.
	+ moneyGraphData: An object consisting of a data array and a settings object.

+ Parameters
	+ instance_no (required, number) - instance number of the consumer accessing app

#### Get the graph data [GET]

+ Response 200 (application/json)

		+ Body
			{
			  "graphData": {
			    "co2GraphData": {
			      "data": [ { ... }, { ... } ], 
			      "settings": { ...  }
			    }, 
			    "localGraphData": { "benchmark": 35, "title": "null", "value": 45 }, 
			    "moneyGraphData": {
			      "data": [ { ... }, { ... } ], 
			      "settings": { ...  }
			    }
			  }
			}





## GROUP Data Labs


### GROUP Data [/labs/data]
-------------------------------

### KPIs for Pilot Test [/labs/data/testKpis]
---
KPIs and pure number statistics for assessing the test generally.

+ Array with 6 elements, each containing 3-element (title, value, unit) arrays with data for:
	+ Sign-ups
	+ SMS Messages Sent
	+ SMS Replies
	+ Impact Points Awarded
	+ CO2 Footprint Reduced
	+ Consumption Reduced
	+ Consumption Shifted

#### View All [GET]

+ Response 200 (application/json)

		+ Body
				[
				  ["Sign-ups", 52, ""], 
				  ["SMS Messages Sent", 1099, ""],
				  ["SMS Replies", 714, ""], 
				  ["Impact Points Awarded", 3058, ""],
				  ["CO2 Footprint Reduced", 28.468593439999999, "kg CO2-eq"], 
				  ["Consumption Reduced", -135.77014617, "kWh"], 
				  ["Consumption Shifted", 6.6433300000000006, "kWh"] 
				]

### Danish CO2 Value [/labs/data/hourlyCO2Emissions/denmark (/all)]
---
Hourly CO2 emissions of Denmark scraped from energinet.dk Flash page.

+ Array of arrays, each containing 4-elements:
	+ id
	+ Energinet.dk time: ISO8601 timestamp with timezone string
	+ Local system time of recording: IS08601 timestamp without timezone string
	+ CO2 Emissions value

#### View All [GET]	[/all]

+ Response 200 (application/json)

		+ Body
				[
					[1, "2016-04-30T18:08:00+00:00", "2016-05-01T00:00:00", 327.0], 
					[2, "2016-04-30T23:08:00+00:00", "2016-05-01T01:00:00", 308.0], 
					[3, "2016-05-01T00:08:00+00:00", "2016-05-01T02:00:00", 317.0],
					...
				] 

#### Update [POST]


### GROUP Graphs [/labs/graphs]
-------------------------------
### Changes in consumption due to activity[/labs/graphs/consumptionChange]
---
	### Morning [/labs/graphs/consumptionChange/morning]
	---
	Changes in consumption due to messages sent regarding Morning activity.

	+
		#### View All [GET]			

	### Messages sent, replies, reply rate [/labs/graphs/messages/daywise]
	---
		#### View All [GET]	



### GROUP Graphs [/labs/graphs]
-------------------------------



## GROUP Cron Scripts
