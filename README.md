# DEZ-Homework1
Homework for Docker+SQL Module

# Answers

## Question 1. Understanding Docker images

We run the command:

```
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim
```

now run: 
```
pip -V
```
to get the pip version:
```
root@1ad4022dd917:/# pip -V
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Question 2. Understanding Docker networking and docker-compose

- Hostname is postgres
- Port is 5432

### Answer: postgres:5432 , db:5432


## Question 3. Counting short trips

### query used:

```
SELECT 
    COUNT(*) 
FROM 
    greentrips_data 
WHERE 
    (lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01')
    AND trip_distance <= 1;
```

The result returned is 8007

