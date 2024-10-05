# Short Answer Questions

## What does Pydantic handle for us?

Pydantic is a python library we use in our application to handel data validation and type management. 
In our API, certain end points require inputs of a certain data type or data values within a certain field range.
For example our longitude and latitude parameters had a certain acceptable range value. Pydantic automatically
handels this for us. Pydantic prevents improper fields to be passed to the machine learning model, while also
preventing runtime errors.


## What do Docker `HEALTHCHECK`s do?

A docker healthcheck are instructions that let the developer know the status of the container. In our project our Docker healthcheck pings the /health endpoint every 30s providing us with a 
realtime update of our container. 

## We removed `uvicorn` and `httpx` from our dependencies; we did not specify `pydantic` in our main dependencies. How were we able to utilize these external libraries?

Many libraries require their own dependencies. FastAPI depends on Pydantic, Starlette and uvicorn to work. Pydantic handles data validation and type management, while Starlette handles the core functionality of FastAPI, uvicorn makes it our code accessible over the internet. Starlette depends on httpx for testing HTTP clients.
So even thought we do not explicitly have uvicorn and httpx listed in our dependencies they are transitive dependencies allowing us to utilize them through other dependencies.