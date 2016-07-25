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
/*----------------------------------------*/

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


/*----------------------------------------*/



## GROUP Data Lab
/*----------------------------------------*/

### GROUP Data [/labs/data]
-------------------------------




### GROUP Graphs [/labs/graphs]
-------------------------------


/*----------------------------------------*/

## GROUP Cron Scripts
/*----------------------------------------*/

/*----------------------------------------*/