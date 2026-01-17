# DEZ-Homework1
Homework for Docker+SQL Module

# Answers

## Question 1. Understanding Docker images
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

### Answer 
We run the command:

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim
```

now run: 
```bash
pip -V
```
to get the pip version:
```bash
root@1ad4022dd917:/ pip -V
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Question 2. Understanding Docker networking and docker-compose

Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

### Answer: postgres:5432 , db:5432


## Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?


### query used:

```sql
SELECT 
    COUNT(*) 
FROM 
    greentrips_data 
WHERE 
    (lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01')
    AND trip_distance <= 1;
```
#### The result returned is 8007


## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.
query used:
```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE) AS pickup_day,
    MAX(trip_distance) AS maximum_distance
FROM 
    greentrips_data
WHERE 
    trip_distance < 100
GROUP BY
    CAST(lpep_pickup_datetime AS DATE)
ORDER BY 
    maximum_distance DESC
LIMIT 1;

| pickup_day | maximum_dist |
|------------+--------------|
| 2025-11-14 | 88.03        |
```
#### The date is 2025-11-14


## Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?


query used:
```sql
SELECT 
    g."PULocationID" AS pickup_loc,
    t."Zone" AS pickup_zone,
    SUM(g.total_amount) AS total_amount
FROM
    greentrips_data g
JOIN 
    taxi_zones t ON g."PULocationID" = t."LocationID"
WHERE 
    CAST(g.lpep_pickup_datetime AS DATE) = '2025-11-18'
GROUP BY 
    g."PULocationID", t."Zone"
ORDER BY 
    total_amount DESC
LIMIT 1;

| pickup_loc | amt          | pickup_zone      |
|------------+--------------+-----------------|
| 74  | 88.9281.920000000004| East Harlem North|

```

#### The Zone is East Harlem North

## Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.
query used:
```sql
SELECT 
     t_drop."Zone" AS dropoff_zone,
     g.tip_amount AS largest_tip
 FROM 
    greentrips_data g
 JOIN 
    taxi_zones t_pickup ON g."PULocationID" = t_pickup."LocationID"
 JOIN 
    taxi_zones t_drop ON g."DOLocationID" = t_drop."LocationID"
 WHERE 
    t_pickup."Zone" = 'East Harlem North'
    AND 
        CAST(g.lpep_pickup_datetime AS DATE) >= '2025-11-01'
    AND 
        CAST(g.lpep_pickup_datetime AS DATE) < '2025-12-01'
 ORDER BY 
    g.tip_amount DESC
 LIMIT 1;



| dropoff_zone   | largest_tip |
|------------+-----------------|
| Yorkville West | 81.89       |

```
#### The Zone is Yorkville West