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
