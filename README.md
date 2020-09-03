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

