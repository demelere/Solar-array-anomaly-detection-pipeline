ML model and pipeline and data api for identifying efficiency loss, degradation, and anomalous behavior in the International Space Station Roll Out Solar Array cells (i.e. iROSA).

### Data API
Data API for storing and accessing the solar array telemetry data.  This is naive to the upstream part of the pipeline that ingests and delivers data from the sensors to the database.  Instead, it contains dummy seed data for demonstration purposes in a time-series database (TimeScaleDB), containerized with Docker Swarm and hosted on AWS EC2 with a Flask endpoint.

### Exploration of methods
Candidate models for solar panel data anomaly/fault detection, which is a specialized time series challenge.

Time series methods:
* Deviation from the mean
* Support Vector Machines
* K Means Clustering
* ARIMA
* Mahalanobis Distance 

Machine learning methods:
* k-Nearest Neighbors
* CatBoost
* XGBoost
* Principal Component Analysis
* Isolation Forest

Deep learning methods:
* Autoencoder

Physical model approaches:
* Horizontal radiation and humidity

Computer vision approaches
* CNN, etc for the panel imagery

### Development

* Activate virtual environment in `ml-model` with `source venv/bin/activate` and `deactivate`
* Cmd+shift+p in VSCode to select environment for notebook

#### Deploy models in an ML pipeline
Use AWS Sagemaker to process data (Processing, Training, Tuning Step), evaluate and register data (Processing, Condition, and Model steps), deploy the model (Lambda Function and Custom Endpoint), and monitor the model.