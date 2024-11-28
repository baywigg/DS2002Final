# DS2002 ETL Pipeline

**First, open a terminal and ensure you have Python 3.11 installed**

`python3 --version`

If not, install it from the official Python website.

### Navigate to the root project directory at DS2002Final/

**Next, create and activate a virtual environment to install the required packages**

`python3.11 -m venv venv`

`source venv/bin/activate`

**Install required packages after ensuring pip is updated**

`pip install --upgrade pip`

`pip install -r requirements.txt`

### We will now set up our environmental variables

**Create a folder called exactly '.env' in the root directory (DS2002Final/) either with your editor or by running**

`touch .env`

**Add these three values to the newly created '.env' file, with your MySQL credentials in place of <YOUR_PASSWORD>**

```
DB_USER="root"
DB_PASSWORD="<YOUR_PASSWORD>"
DB_HOST="localhost"
```

**Finally, ensure your MySQL instance is running by navigating to the MySQL Workbench and attempting to connect.**

## After all this is complete, you can run the ETL Pipeline with

`python3 ETLPipeline/main.py`
