# Event-Detection-Engine - DIPET

Event Detection Engine for the DIPET Chist-Era project based on the work done during the DICE H2020 project specifically the [DICE Anomaly Detection Platform.](https://github.com/dice-project/DICE-Anomaly-Detection-Tool)
and on the work done during the [ASPIDE](https://www.aspide-project.eu/) H2020 project.

## Context

In the following section we will use the term events and anomalies seemingly interchangeably. 
However, we should note that the methods used for detecting anomalies are applicable in the case of events. 
The main difference lies in the fact that anomalies pose an additional level of complexity by their spars nature, 
some anomalies might have an occurrence rate well under 0.01%.
Event and anomaly detection can be split up into several categories based on the methods and the characteristics of 
the available data. The most simple form of anomalies are point anomalies which can be characterized by only one metric (feature). 
These types of anomalies are fairly easy to detect by applying simple rules (i.e. CPU is above 70%). Other types of anomalies 
are more complex but ultimately yield a much deeper understanding about the inner workings of a monitored exascale system or application. 
These types of anomalies are fairly common in complex systems.

Contextual anomalies are extremely interesting in the case of complex systems. These types of anomalies happen when a 
certain constellation of feature values is encountered. In isolation these values are not anomalous but when viewed in 
context they represent an anomaly. These type of anomalies represent application bottlenecks, imminent hardware failure 
or software miss-configuration. The last major type of anomaly which are relevant are temporal or sometimes sequential 
anomalies where a certain event takes place out of order or at the incorrect time. These types of anomalies are very 
important in systems which have a strong spatio-temporal relationship between features, which is very much the case for exascale metrics.


## Architecture

The Event detection engine (**EDE**) has several sub-components which are based on lambda type architecture where we have a 
_speed_, _batch_ and _serving_ layer. Because of the heterogeneous nature of most modern computing systems (including exascale and mesh networks) 
and the substantial variety of solutions which could constitute a monitoring services the _data ingestion component_ has to be 
able to contend with fetching data from a plethora of systems. _Connectors_ is implemented such that it  serves as adapters for each solution. 
Furthermore, this component also is be able to load data directly from static file (_HDF5_, _CSV_ , _JSON_, or even _raw format_). 

![EDE Architecture](https://github.com/DIPET-UVT/EDE-Dipet/blob/master/architecture/ede_arch_v3-Page-2.png)

This aids in fine tuning of event and anomaly detection methods. We can also see that _data ingestion can be done directly_ 
via query from the monitoring solution or _streamed directly from the queuing service_ (after ETL if necessary). 
This ensures that we have the best chance of reducing the time between the event or anomaly happening and it being detected.

The _pre-processing component_ is in charge of taking the raw data from the data ingestion component and apply several transformations. 
It handles _data formatting_ (i.e. one-hot encoding), _analysis_ (i.e. statistical information), _splitter_ (i.e. splitting the 
data into training and validation sets) and finally _augmentation_ (i.e. oversampling and undersampling). 

As an example the analysis and splitter are responsible for creating stratified shuffle split for K-fold cross
validation for training while the augmentation step might involve under or oversampling techniques such as ADASYN or SMOTE. 
This component is also responsible for any feature engineering of the incoming monitoring data.

The _training component_ (batch layer) is used to instantiate and train methods that can be used for event and anomaly detection. 
The end user is able to configure the hyper-parameters of the selected models as well as run automatic optimization on these (i.e. Random Search, Bayesian search etc.). 
Users are not only able to set the parameters to be optimized but to define the objectives of the optimization. 
More specifically users can define what should be optimized including but not limited to predictive performance, 
_transprecise_ objectives (inference time, computational limitations, model size etc.).

_Evaluation_ of the created predictive model on a holdout set is also handled in this component. 
Current research and rankings of machine learning competitions show that creating an _ensemble_ of 
different methods may yield statistically better results than single model predictions. Because of this 
ensembling capabilities have to be included.
 
Finally, the trained and validated models have to be saved in such a way that enables them to be easily instantiated and used in a production environment. 
Several predictive model formats have to be supported, such as; PMML, ONNX, HDF5, JSON.

It is important to note at this time that the task of event and anomaly detection can be broadly split into two main types of machine learning tasks; 
classification and clustering. Classification methods such as Random Forest, Gradient Boosting, Decision Trees, Naive Bayes, Neural networks, Deep Neural Networks 
are widely use in the field of anomaly and event detection. While in the case of clustering we have methods such as IsolationForest, DBSCAN and Spectral Clustering.
Once a predictive model is trained and validated it is saved inside a model repository. Each saved model has to have 
metadata attached to it denoting its performance on the holdout set as well as other relevant information such as size, throughput etc.
 
The _prediction component_ (speed layer) is in charge of retrieving the predictive model form the model repository and feed metrics from the monitored  system. 
If and when an event or anomaly is detected EDE is responsible with signaling this to both the Monitoring service reporting component and to other tools such as the 
Resource manager and/or scheduler any decision support system. Figure 1 also shows the fact that the prediction component gets it’s data from both 
the monitoring service via direct query or directly from the queuing service via the data ingestion component.

For some situations a rule based approach is better suited. For these circumstances the prediction component has to include a rule based engine and a rule repository.
Naturally, detection of anomalies or any other events is of little practical significance if there is no way of handling them. 
There needs to be a component which once the event has been identified tries to resolve the underlying issues. 

## Utilization

EDE is designed around the utilization of a yaml based configuration scheme. This allows the complete configuration of the tool by the end user with limited to no intervention in the source code.
It should be mentioned that some of these features are considered unsave as they allow the execution of arbitrary code.  
The configuration file is split up into several categories:
* **Connector** - Deals with connection to the data sources
* **Mode** - Selects the mode of operation for EDE
* **Filter** - Used for applying filtering on the data
* **Augmentation** - User defined augmentations on the data
* **Training** - Settings for training of the selected predictive models
* **Detect** - Settings for the detection using a pre-trained predictive model
* **Point** - Settings for point anomaly detection
* **Misc** - Miscellaneous settings

### Connector

The current version of EDE support 3 types of data sources: _ElasticSearch_, _Prometheus_ and _CSV/Excel_. Conversely it supports also reporting mechanisms for ElasticSearch and Kafka.
In the former case, a new index is created in ElasticSearch which contains the detected anomalies while in the latter a new Kafka topic is created where the detected anomalies are pushed.

This sections parameters are:
* _PREndpoint_ - Endpoint for fetching Prometheus data
* _ESEndpoint_ - Endpoint for fetching ElasticSearch data
* _MPort_ - Sets the monitoring port for the selected Endpoint (defaults to 9200)
* _KafkaEndpoint_ - Endpoint for a pre existing Kafka deployment
* _KafkaPort_ - Sets the Kafka port for the selected Kafka Endpoint (defaults to 9092)
* _KafkaTopic_ - Name of the kafka topic to be used
* _Query_ - The query string to be used for fetching data:
    * In the case of ElasticSearch please consult the official [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html).
    * In the case of Prometheus please consult the official [documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
        * For fetching all queryable data:  `{"query": '{__name__=~"node.+"}[1m]'}`
        * For fetching specific metric data: `{ "query": 'node_disk_written_bytes_total[1m]'}`
* _MetricsInterval_ - Metrics datapoint interval definition
* _QSize_ -  size in MB of the data to be feteched (only if ESEndpoint is used)
    * For no limit use `QSize: 0`
* _Index_ - The name of the column to be set as index
    * The column has to have unique values, by default it is set to the column denoting the time when the metric was read
* _QDelay_ - Polling period for metrics fetching
* _Dask_
    * _ScheduelerEndpoint_ - Denotes the Dask scheduler endpoint
        * If no pre-deployed Dask instance is available EDE can deploy a local Scheduler by setting this parameter to `local`
    * _SchedulerPort_ -  Endpoint for Dask scheduler endpoint
    * _Scale_ - Sets the number of workers if `local` scheduler is used
    * _EnforceCheck_ - if set to true it will check if the libraries from the python environment used on each Dask worker are the same versions as the origination source
        * If this check fails the job will exit with an error message
        * This parameter can be omitted in the case of local deployment
     

**Notes**: 
* Only one of type of connector endpoint (PREndpoint or ESEndpoint) is supported in any given time.

###Mode

The following settings set the mode in which EDE operates. There are 3 modes available in this version; _Training_, _Validate_, _Detect_

* _Training_ - If set to true a Dask worker or Python process for training is started
* _Validate_  - If set to true a Dask worker or Python process for validation is started
* _Detect_ - If set to true a Dask worker for Python process fof Detection is started

**Notes:**
* In case of a local Dask deployment it is advised to have at least 3 workers started (see the _Scale_ parameter in the previouse section). 

### Filter

