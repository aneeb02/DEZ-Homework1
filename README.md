# DEZ-Homework1
Homework for Docker+SQL Module

# Answers

## Question 1. Understanding Docker images

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

- Hostname is postgres
- Port is 5432

### Answer: postgres:5432 , db:5432


## Question 3. Counting short trips

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

```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE) AS pickup_day,
    MAX(trip_distance) AS maximum_distance
FROM greentrips_data
WHERE trip_distance < 100
GROUP BY CAST(lpep_pickup_datetime AS DATE)
ORDER BY maximum_distance DESC
LIMIT 1;

| pickup_day | maximum_dist |
|------------+--------------|
| 2025-11-14 | 88.03        |
```
#### The date is 2025-11-14

