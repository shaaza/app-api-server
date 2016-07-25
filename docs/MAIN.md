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
			#### View all [GET]

	### GROUP Graphs
	-------------------------------

		### Goal Graph Data [/app/graphs/selectGoal/{instance_no}]
		---
			#### View [GET]

		### Activities Goal Graph Data [/app/graphs/selectActivity/{instance_no}]
		---
			#### View [GET]

/*----------------------------------------*/



## GROUP Data Lab
/*----------------------------------------*/

	### GROUP Data [/labs/data]
	-------------------------------

		### Danish CO2 Value [/labs/data/co2]
		---
			#### View All [GET]	

			#### Update [POST]

		### KPIs for Pilot Test [/labs/data/kpis]
		---
			#### View All [GET]	

	### GROUP Graphs [/labs/graphs]
	-------------------------------
		### Changes in consumption due to activity[/labs/graphs/consumptionchange]
		---
			#### View All [GET]			

		### Messages sent, replies, reply rate [/labs/graphs/messages/all]
		---
			#### View All [GET]	

/*----------------------------------------*/

## GROUP Cron Scripts
/*----------------------------------------*/
		### Update DB with data in EngazeDataSe.csv  [/cron/updateDatabase]
		---
			#### Run update script [POST]			

		### Copy file EngazeDataSe.csv into local storage [/cron/backup/data/{time}]
		---
			#### Run copy [POST]	

/*----------------------------------------*/