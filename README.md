# analyzing-network-traffic_kdd99
Tovio Roberts - Galvanize Data Science Analytics capstone

# Overview

## Questions:
- What with feature engineered (Y-derived) data?
- Why might it be worthwhile to make categorical predictions on derived features?
- What would my next steps be?

## What I did
- Explored the kdd99 data
- Tested significant differences in ratios of attack category
- Applied a logistic regression model to discern 1 category
- Compared performance of single features through the model

## About the original competition
The data come from a machine learning competition held in 1999.  See http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html .  Essentially, the task was to create a predictive model able to categorize a wide variety of bad connections or attacks into four main categories.  Additionally, malicious connections should be categorized separately from "normal" connections.

## Workflow
- leveraged bash to pull arbitrary numbers of random samples from the data
  - (>700000 rows)
  - quick visualization and sanity checks
- abstracted functions into relevant classes
  - reusability
  - not trapped in jupyter
- Tried out a lot of things, abandoned almost everything

# Exploratory Data Analysis

## What is unique about this data?
  - It was generated artificially and shared incrementally as TCP dumps, totalling roughly 4GB in total.
  - Many of the 42 features were derived and interrelated with the predictant
  - A basic logistic regression model, given a set of features with < |0.60| correlation will easily predict on the training data at "too high" an accuracy.

## The Data
- no null values
- mix of numeric and categorical types
- smurf attacks (DOS) comprise 57% of the rows
- many types of values for
  - service
  - flag

![Too Much Smurf](/images/too_much_smurf.png)

# Thus...

![ICMP Supreme](/images/icmp_supreme.png)
- `ICMP` - (from wikipedia): is used by network devices, including routers, to send error messages and operational information indicating, for example, that a requested service is not available or that a host or router could not be reached. `ICMP` differs from transport protocols such as `TCP` and `UDP` in that it **is not typically used to exchange data** between systems, nor is it regularly employed by end-user network applications
## Protocol Types
```
icmp    405033
tcp     267370
udp      27597
```
- Keep in mind that many attack types only happen over certain protocols.

![ICMP Attack Labels](/images/attack_names_by_icmp.png)
![ICMP Attack Labels](/images/attack_names_by_tcp.png)
![ICMP Attack Labels](/images/attack_names_by_udp.png)


## No Clear Distributions of Features

  ### High zero-only values for some columns:
  ```
  At 700000 samples:
   land has only zero values
   num_outbound_cmds has only zero values
   is_host_login has only zero values
  ```
  ### Other features have weird distributions
  ![Weird Distribution](/images/weird_distribution.png)





## Correlation
#### How helpful is this Correlation Matrix?
![Raw Correlation Matrix](/images/correlation_matrix_before.png)

#### Not as helpful as a list of high correlations:
```
{('count', 'dst_host_same_src_port_rate'): 0.862
 ('dst_host_rerror_rate', 'dst_host_srv_rerror_rate'): 0.987
 ('dst_host_rerror_rate', 'srv_rerror_rate'): 0.985
 ('dst_host_same_src_port_rate', 'dst_host_same_srv_rate'): 0.676
 ('dst_host_same_src_port_rate', 'dst_host_srv_count'): 0.684
 ('dst_host_same_src_port_rate', 'same_srv_rate'): 0.668
 ('dst_host_same_src_port_rate', 'srv_count'): 0.947
 ('dst_host_same_srv_rate', 'dst_host_srv_count'): 0.979
 ('dst_host_same_srv_rate', 'srv_count'): 0.694
 ('dst_host_serror_rate', 'dst_host_srv_serror_rate'): 0.998
 ('dst_host_serror_rate', 'serror_rate'): 0.998
 ...
```

## Putting attack labels into buckets

### Attack labels fall into 4 main categories:
  0. Normal: not an attack
  1. Probe: surveillance and other probing, e.g., port scanning
  2. DOS: denial-of-service, e.g. syn flood
  3. U2R:  unauthorized access to local superuser (root) privileges, e.g., various `buffer overflow`` attacks
  4. R2L: unauthorized access from a remote machine, e.g. guessing password;

  - **20 types of attack (labels) to be categorized for training**
  ![Attack labels per category](/images/attack_labels_per_category.png)
    - **0 - Normal: 139294 categorized**
    - **1 - Probe: 5833 categorized**
    - **2 - DOS: 554699 categorized**
    - **3 - U2R: 8 categorized**
    - **4 - R2L: 166 categorized**


# Hypothesis Tests

#### Question: Are the proportions of connections that are attacks ( that fall into the attack category, not normal) consistent across protocol types?
- recall that `normal.` is not an attack.
- we will use the general category to get counts

From the graphics above, it seems likely that ICMP garners a higher proportion of attacks than TCP or UDP. We can perform a chi-squared test for proportions to check if there is a statistical difference.
- ALPHA = 0.05
- df = 1
- total sample size: 700000

**Determine the proportion of attacks/connection for each protocol_type**
#### ICMP
```
Number of icmp Connections: 405033
Number of Attacks: 403238
Number Normal: 1795
Cat   Count
2    401455
0      1795
1      1783
```
#### TCP
```
Number of tcp Connections: 267832
Number of Attacks: 157741
Number Normal: 110091
Cat   Count
2    153805
0    110091
1      3762
4       166
3         8
```
#### UDP
```
Number of udp Connections: 27850
Number of Attacks: 413
Number Normal: 27437
Cat   Count
0    27437
1      279
2      134
```
## Test ICMP vs TCP attack proportion
- H0: the proportion of connections recorded that are attacks is not significantly different between ICMP and TCP
- HA: the proportion of connections recorded that are attacks is significantly different betwwen ICMP and TCP
- ALPHA = 0.05
- df = 1

  **perform chi-square test for proportion**
```python
from scipy.stats import chi2_contingency
obs = np.array([[icmp_obs_attacks,
      icmp_obs_normal],[tcp_obs_attacks, tcp_obs_normal]])
chi2, p, dof, expected = chi2_contingency(obs)
```
#### RESULTS:
```
Reject H0, there is a significant difference in attack/connection proportion between ICMP and TCP
chi-square test statistic: 192072.97
           p-value       : 0.00
           deg of freedom: 1.00
```

## Test TCP vs UDP attack proportion
- H0: the proportion of connections recorded that are attacks is not significantly different between TCP and UDP
- HA: the proportion of connections recorded that are attacks is significantly different between TCP and UDP
- ALPHA = 0.05
- df = 1

  **perform chi-square test for proportion**

#### RESULTS
```
Reject H0, there is a significant difference in attack/connection
           proportion between TCP and UDP
chi-square test statistic: 33421.43
           p-value       : 0.00
           deg of freedom: 1.00
```

### Further test to perform:
- Create filters of services
- Test if proportions of services:attack types are significantly different
- Use top 10 count of services, so 10-row chi test

# Modeling

## I chose to only model for one category of attack
  - Since denial of service floods servers with response requests, it was the majority category of attack type.

## Transforming the data
- split target into 1 for DOS and 0 for everything else
- wrote methods to auto-drop any features with >.60 correlation coefficients
- dropped rows of the majority class to get 50/50 spread of Y values
![Correlation After](/images/correlation_after.png)


## Wrote utilities to model each feature independently
  - populate pandas dataframe with confusion matrix values
  - output metrics on each feature



## Logistic Regression Results:
```
#--------------------------------------------#
     Running classifier on ['duration']
#--------------------------------------------#


Modified Y to balance 1s and 0s
1    145236
0    145236
Name: attack_category, dtype: int64


True Positives: 29159
True Negatives: 2322
False Positives: 26614
True Negatives: 0

Accuracy: 0.5418882864274034
Classification_error: 0.4581117135725966
Recall: 1.0
Precision: 0.5228156993527334
False Negative Rate: 0.0

confusion matrix
[[ 2322 26614]
 [    0 29159]]

```


```

 #--------------------------------------------#
      Running classifier on ['service']
 #--------------------------------------------#


 Modified Y to balance 1s and 0s
 1    145236
 0    145236
 Name: attack_category, dtype: int64


 True Positives: 28989
 True Negatives: 26437
 False Positives: 2551
 True Negatives: 118

 Accuracy: 0.9540580084344608
 Classification_error: 0.0459419915655392
 Recall: 0.9959459923729687
 Precision: 0.9191185795814838
 False Negative Rate: 0.0040540076270312985

 confusion matrix
 [[26437  2551]
  [  118 28989]]
```
## Accuracy of Each Feature
![Single Feature Accuracy](/images/single_feature_accuracy.png)

## False Negative Rate of Each Feature
![Single Feature Accuracy](/images/single_feature_false_negative.png)


# Bringing this into the world
- How well can `derived features` be discerned in real time?
  - How few do you need to make a good guess
  - What is the computation cost on the derivation of any given feature in real time

# What I did
- attempted to apply lasso, with little success
  - instead incorporated `l1` into `LogisticRegression(penalty='l1')`
- built a pipeline, scrapped it in favor of utilities that call each other

# What I would like to add
- Fit the model to the other categories
- Apply the model to the actual test data
- Combinations on the features, and
- Cost matrix for the theoretical ramifications of False Negatives

## Features in the raw dataset

|feature name	|description 	|type|
|-----------|---------------|----|
|duration| 	length (number of seconds) of the connection 	| continuous
|protocol_type| 	type of the protocol, e.g. tcp, udp, etc. |	discrete
|service| 	network service on the destination, e.g., http, telnet, etc. |	discrete
|src_bytes| 	number of data bytes from source to destination 	| continuous
|dst_bytes |	number of data bytes from destination to source 	| continuous
|flag |	normal or error status of the connection 	| discrete
|land| 	1 if connection is from/to the same host/port; 0 otherwise 	|discrete
|wrong_fragment| 	number of ``wrong'' fragments |	continuous
|urgent| 	number of urgent packets |	continuous

## Basic features of individual TCP connections.

|feature name	|description 	|type|
|-----------|---------------|----|
|hot |	number of ``hot'' indicators	| continuous
|num_failed_logins| 	number of failed login attempts |	continuous
|logged_in |	1 if successfully logged in; 0 otherwise |	discrete
|num_compromised |	number of ``compromised'' conditions |	continuous
|root_shell | 1 if root shell is obtained; 0 otherwise |	discrete
|su_attempted |	1 if ``su root'' command attempted; 0 otherwise 	| discrete
|num_root |	number of ``root'' accesses |	continuous
|num_file_creations |	number of file creation operations |	continuous
|num_shells 	|number of shell prompts |	continuous
|num_access_files |	number of operations on access control files 	| continuous
|num_outbound_cmds	|number of outbound commands in an ftp session 	| continuous
|is_hot_login |	1 if the login belongs to the ``hot'' list; 0 otherwise |	discrete
|is_guest_login |	1 if the login is a ``guest''login; 0 otherwise 	|discrete

**for more info: http://kdd.ics.uci.edu/databases/kddcup99/task.html**
