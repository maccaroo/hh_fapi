hh_fapi
=======

The API layer for the Home Historian system, implemented in FastAPI. 

# Purpose
This project is being used to learn FastAPI, and API design patterns.

# What does it do?
Home Historian is a system for the collection of time-series data from around the home.  The schema contains the following tables:
* User - Users of the system
* Data - Some items of data to be tracked.
* DataPoint - Points for some `Data`.
* Meta - Metadata information.
* DataMeta - `Meta` information for some `Data`.

# What requirements are there?
Your system must have Python 3 installed, as well as a database.  The implementation uses Postgres, but you can swap that out to use SqLite3 or some other database if you like.

# How to run it?
## Locally
To run this on your local machine, follow these steps:

Install Python 3 and pip
Update pip
```bash
pip install --upgrade pip
```
Run the server
```bash
python -m app.api.main
```

Alternatively, you can run the web server directly
```bash
uvicorn app.main:app --reload
```

## Remote Server
To run this on a Linux server (like a Raspberry Pi), follow these steps:

SSH to the server
```bash
ssh user@server
```
Update packages
```bash
sudo apt update && sudo apt upgrade -y
```
Install Python3
```bash
sudo apt install python3 python3-pip -y
```
Install Postgres
```bash
sudo apt install -y postgresql postgresql-contrib
```
Change your path to the code folder
```bash
cd /path/to/my/code
```
Create and source virtual env
``` bash
python3 -m venv fastapi_env
source fastapi_env/bin/activate`
```
Install project requirements
```bash
pip install -r requirements.txt
```
Start the server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Navigate to `http://{server_address}:8000` to see the application.

In order to keep the service running, we can use `systemd`.

Create a service file
```bash
sudo nano /etc/systemd/system/home_historian.service
```
Enter the following content
```
[Unit]
Description=Home Historian API Service
After=network.target

[Service]
User=sam
WorkingDirectory=/home/sam/development/workspaces/hh_fapi
ExecStart=/home/sam/development/workspaces/hh_fapi/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Restart=always

[Install]
WantedBy=multi-user.target
```
Reload systemd, enable and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable home_historian.service
sudo systemctl start home_historian.service
```
If later you need to reload the config or service, use the following
```bash
sudo systemctl daemon-reload
sudo systemctl restart home_historian.service
sudo systemctl status home_historian.service
```

# Setup Postgres
In order to get going, you will need to create a database and schema.  The database name is up to you - I will use `home_historian`.
```bash
sudo -i -u postgres
psql
```
Create a user
```sql
CREATE USER hh_user WITH password 'my_super_secret_password';
GRANT ALL PRIVILEGES ON DATABASE home_historian TO hh_user;
```
List users
```sql
\du
```
Create the database
```sql
CREATE DATABASE home_historian;
```
List the databases
```sql
\l
```
Change to our database
```sql
\c home_historian
```
Create our schema
```sql
CREATE SCHEMA hh;
GRANT USAGE, CREATE ON SCHEMA hh TO hh_user;
```
List the schemas
```sql
\dn
```

I use the application-specific user `hh_user` to access the database (instead of the default user `postgres`).  This is more secure, but I've run into issues with database objects which were created with the `postgres` user.  Since access is limited to the schema `hh`, you can run the following script to grant access to `hh_user` for objects it needs:
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA hh TO hh_user;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA hh TO hh_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA hh TO hh_user;
```
You can run the following script to ensure that `hh_user` gets the necessary privileges for new objects:
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA hh GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hh_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hh GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO hh_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hh GRANT EXECUTE ON FUNCTIONS TO hh_user;
GRANT USAGE, CREATE ON SCHEMA hh TO hh_user;
```

# Docker
The API can be deployed on docker with the following steps:

Build the API image
```bash
docker build -t hh-api .
```
Run the services
```bash
docker-compose up -d
```
