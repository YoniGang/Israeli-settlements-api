# Israeli settlements api

## How to start

1. Clone the project
2. Go the the project folder and run in the terminal: "docker-compose build"
3. Then run: "docker-compose up".
4. Now you should see of all the tables in the db ready to get data.

## DB structure
1. I chose to create a different table for the cities, so we will not duplicate the city data for every row in the settlements table.
2. I chose to create the age ranges as columns and not different table because othewise, we will have much more rows per city and the db will be full much faster.
3. I chose to create async session to make the latency faster so the db can still serve while reading and writing.

## API Reference

#### Init data

```http
  GET /init
```
To get all of the data from the governments site to our db

#### Get settlements example

```http
  GET /settlements?month=3&year=2024&min_age=4&max_age=5&min_population=3000
```
The Data Serving API