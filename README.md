# MV Sims #

## Overview
A simple tool used for view historical data of SIM data usage for MyVends customers. Allows filtering by time and ICCID. Uses chart.js for visual display. Docker compose is leveredged with 3 containers. One runs the backend for the webpage, another container runs the database, additionally a third container is used to run an API script that fetches data usage information from the Monogato API on an hourly basis.

[![Screenshot 1](https://i.ibb.co/8zqqFxC/Screenshot-2024-10-21-at-9-17-11-PM.png)](https://ibb.co/rbYYnpj)
[![Screenshot 2](https://i.ibb.co/WWf5CS4/Screenshot-2024-10-21-at-9-18-12-PM.png)](https://ibb.co/wN4gtDF)




## Technologies used
- ** Django **
- ** Postgresql **
- ** Chart.js **
- ** Docker Compose **


## Setup
1. `cd mvsims`
2. `docker compose up --build -d`
3. visit http://localhost:8000/




