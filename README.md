# Israeli settlements api

## How to start

1. Clone the project
2. Go the the project folder and run in the terminal: "docker-compose build"
3. Then run: "docker-compose up".
4. Now you should see of all the tables in the db ready to get data.
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