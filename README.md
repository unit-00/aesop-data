# storyteller-data
storyteller-data is the pipeline to collect data for the machine learning portion. Custom crawler can be written fit into the pipeline for data to be inserted into the warehouse.

# Getting Started
This scraper does require MongoDB to be installed to have documents inserted.

## Setup
Mongo needs to be setup. Docker is recommended. 

Mongo image can be setup with 

```bash
docker run --name some-name -d -p 27017:27017 mongo
```

Clone the repo first.
```bash
git clone git@github.com:unit-00/storyteller-data.git
```

storyteller-data is written on Python 3.7.9 and uses pip-tools for setup:

```bash
pip install pip-tools && pip-sync
```

Be sure to remember to setup a virtual environment to keep things separated.

## Usage
Bash scripts have been prepared for ease of running.

```bash
. tasks/run_pipeline.sh
```

Test has been prepared as well

```bash
. tasks/test_functionality.sh
```

After `tasks/run_pipeline.sh` have been run, the pipeline will insert the collected information in the database.

