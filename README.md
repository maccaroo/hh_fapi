hh_fapi
=======

The API layer for the Home Historian system, implemented in FastAPI. 

# Purpose
This project is being used to learn FastAPI, and API design patterns.

# What does it do?
Home Historian is a system for the collection of time-series data from around the home.  Initially the schema contains only sensors and their readings.

# What requirements are there?
Your system must have Python 3 installed, as well as a database.  The implementation uses Postgres, but you can swap that out to use SqLite3 or some other database if you like.

# How to run it?
## Locally
To run this on your local machine, follow these steps:

Install Python 3 and pip
Update pip: 
```bash
pip install --upgrade pip
```
Run the web server: 
```bash
uvicorn app.main:app --reload
```

## Remote Server
To run this on a Linux server (like a Raspberry Pi), follow these steps:

SSH to the server: 
```bash
ssh user@server
```
Update packages: 
```bash
sudo apt update && sudo apt upgrade -y
```
Install Python3: 
```bash
sudo apt install python3 python3-pip -y
```
Install Postgres:
```bash
sudo apt install -y postgresql postgresql-contrib
```
Change your path to the code folder
```bash
cd /path/to/my/code
```
Create and source virtual env:
``` bash
python3 -m venv fastapi_env
source fastapi_env/bin/activate`
```
Install project requirements:
```bash
pip install -r requirements.txt
```
Start the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Navigate to `http://{server_address}:8000` to see the application.

In order to keep the service running, we can use `systemd`:

Create a service file:
```bash
sudo nano /etc/systemd/system/fastapi.service
```
Enter the following content:
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
Reload systemd, enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl start fastapi.service
```

# Setup Postgres
In order to get going, you will need to create a database and schema.  The database name is up to you - I will use `home_historian`.
```bash
sudo -i -u postgres
psql
```
Create a user:
```sql
CREATE USER hh_user WITH password 'my_super_secret_password';
GRANT ALL PRIVILEGES ON DATABASE home_historian TO hh_user;
```
List users:
```sql
\du
```
Create the database:
```sql
CREATE DATABASE home_historian;
```
List the databases:
```sql
\l
```
Change to our database:
```sql
\c home_historian
```
Create our schema:
```sql
CREATE SCHEMA hh;
GRANT USAGE, CREATE ON SCHEMA hh TO hh_user;
```
List the schemas:
```sql
\dn
```
