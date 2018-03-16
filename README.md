# analyzing-network-traffic_kdd99
Tovio Roberts - Galvanize Data Science Analytics capstone

# Overview

## Questions:
- What do you do with directly correlated/Y-derived data?
- Why might it be worthwhile to make categorical predictions on derived features?

<br><br><br><br>
--------------------------------
## What I did
- Explored the kdd99 data
- Tested significant differences in ratios of attack categories
- Downsampled majority class
- Applied a logistic regression model to single features in order to compare False Negative and Accuracy rates

<br><br><br><br><br><br><br><br>
--------------------------------
## The original KD99 competition
- The data come from a machine learning competition held in 1999.  See http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
- The task was to create a predictive model able to categorize a wide variety of bad connections or attacks into four main categories.
- Additionally, malicious connections should be categorized separately from "normal" connections.

<br><br><br><br>
--------------------------------

## Workflow
- leveraged bash to pull arbitrary numbers of random samples from the data
  - (>700000 rows)
  - quick visualization and sanity checks
- abstracted functions into relevant classes
  - reusability
  - not trapped in jupyter
- Tried out a lot of things, abandoned almost everything

<br><br><br><br>
--------------------------------

# Exploratory Data Analysis

## What is unique about this data?
  - It was generated artificially and shared incrementally as TCP dumps, totalling roughly 4GB in total.
  - Many of the 42 features were derived and interrelated with the predictant
  - A basic logistic regression model, given a set of features with < |0.60| correlation will easily predict on the training data at "too high" an accuracy.

<br><br><br><br>
--------------------------------

## The Data
- no null values
- mix of numeric and categorical types
- smurf attacks (DOS) comprise 57% of the rows
- many types of values for
  - service
  - flag

<br><br><br><br>
--------------------------------


![Too Much Smurf](/images/too_much_smurf.png)

# Thus...

![ICMP Supreme](/images/icmp_supreme.png)

<br><br><br><br>
-------------------------------

## Protocol Types
```
icmp    405033
tcp     267370
udp      27597
```

- `ICMP` - (from wikipedia): is used by network devices, including routers, to send error messages and operational information indicating, for example, that a requested service is not available or that a host or router could not be reached.
- Keep in mind that many attack types only happen over certain protocols.

<br><br><br><br>
-------------------------------

![ICMP Attack Labels](/images/attack_names_by_icmp.png)

<br><br><br><br>
-------------------------------

![ICMP Attack Labels](/images/attack_names_by_tcp.png)

<br><br><br><br>
-------------------------------

![ICMP Attack Labels](/images/attack_names_by_udp.png)

<br><br><br><br>
-------------------------------

## No Clear Distributions in Features

  ### High zero-only values for some columns:
  ```
  At 700000 samples:
   land has only zero values
   num_outbound_cmds has only zero values
   is_host_login has only zero values
  ```

<br><br><br><br>
-------------------------------

  ### Other features have weird distributions
  ![Weird Distribution](/images/weird_distribution.png)


<br><br><br><br>
-------------------------------

## Correlation
#### How helpful is this Correlation Heatmap?
![Raw Correlation Matrix](/images/correlation_matrix_before.png)

<br><br><br><br>
-------------------------------

#### Not as helpful as a list of high correlations:
```
{('count', 'dst_host_same_src_port_rate'): 0.862
 ('dst_host_rerror_rate', 'dst_host_srv_rerror_rate'): 0.987
 ('dst_host_rerror_rate', 'srv_rerror_rate'): 0.985
 ('dst_host_same_src_port_rate', 'dst_host_same_srv_rate'): 0.676

 ...
```

<br><br><br><br>
-------------------------------



# Hypothesis Tests

### Are the proportions of connections that are attacks consistent across protocol types?
- recall that `normal.` is not an attack.
- we will get counts of normal and everything else

From the graphics above, it seems likely that ICMP garners a higher proportion of attacks than TCP or UDP. We can perform a chi-squared test for proportions to check if there is a statistical difference.
- ALPHA = 0.05
- df = 1
- total sample size: 700000

<br><br><br><br>
-------------------------------

### Proportion of attacks/connections for each protocol_type
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

<br><br><br><br>
-------------------------------

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

<br><br><br><br>
-------------------------------

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

<br><br><br><br>
-------------------------------

## Test ICMP vs TCP attack proportion
- H0: the proportion of connections recorded that are attacks is not significantly different between ICMP and TCP
- HA: the proportion of connections recorded that are attacks is significantly different between ICMP and TCP
- ALPHA = 0.05
- df = 1

<br><br><br><br>
-------------------------------


## Perform chi-square test for proportion
```python
from scipy.stats import chi2_contingency
obs = np.array([[icmp_obs_attacks,
      icmp_obs_normal],[tcp_obs_attacks, tcp_obs_normal]])
chi2, p, dof, expected = chi2_contingency(obs)
```

<br><br><br><br>
-------------------------------


### RESULTS:
```
Reject H0, there is a significant difference
in attack/connection proportion between ICMP and TCP

chi-square test statistic: 192072.97
           p-value       : 0.00
           deg of freedom: 1.00
```

<br><br><br><br>
-------------------------------


## Test TCP vs UDP attack proportion
- H0: the proportion of connections recorded that are attacks is not significantly different between TCP and UDP
- HA: the proportion of connections recorded that are attacks is significantly different between TCP and UDP
- ALPHA = 0.05
- df = 1

<br><br><br><br>
-------------------------------


## Perform chi-square test for proportion

#### RESULTS
```
Reject H0, there is a significant difference in attack/connection
           proportion between TCP and UDP
chi-square test statistic: 33421.43
           p-value       : 0.00
           deg of freedom: 1.00
```

<br><br><br><br>
-------------------------------


## Further test to perform:
- Create filters of services
- Test if proportions of services:attack types are significantly different
- Use top 10 count of services, so 10-row chi test


<br><br><br><br>
-------------------------------

# Modeling

## I chose to only model for one category of attack
  - Since `denial of service` floods servers with response requests, it was the majority category of attack type.
  - Used only a logistic regression
  - Built a reusable template that can take other models
  - Iterated through and gathered Error Type metrics on selected list of features

<br><br><br><br>
-------------------------------


## Attack labels fall into 5  categories:
  0. Normal: not an attack
  1. Probe: surveillance and other probing, e.g., port scanning
  2. DOS: denial-of-service, e.g. syn flood
  3. U2R:  unauthorized access to local superuser (root) privileges, e.g., various `buffer overflow`` attacks
  4. R2L: unauthorized access from a remote machine, e.g. guessing password;
   - (some descriptions of the problem have 5 categories)

<br><br><br><br>
-------------------------------

### Over 20 types of attack to be categorized for model training
  ![Attack labels per category](/images/attack_labels_per_category.png)
  - **0 - Normal: 139294 categorized**
  - **1 - Probe: 5833 categorized**
  - **2 - DOS: 554699 categorized**
  - **3 - U2R: 8 categorized**
  - **4 - R2L: 166 categorized**

<br><br><br><br>
-------------------------------

## Transforming the data
- split target Y into 1 for DOS (Denial of Service) and 0 for everything else
- wrote methods to auto-drop any features with >.60 correlation coefficients
- dropped rows of the majority class to get 50/50 spread of Y values

<br><br><br><br>
-------------------------------
## Better
![Correlation After](/images/correlation_after.png)

<br><br><br><br>
-------------------------------

## Wrote utilities to model list of chosen features, one by one
  - populate pandas dataframe with confusion matrix values
  - output metrics on each feature


<br><br><br><br>
-------------------------------

#### ... on `service`
- network service on the destination, e.g., http, telnet, etc.
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
 False Negatives: 118

 Accuracy: 0.954
 Classification_error: 0.045
 Recall: 0.995
 Precision: 0.919
 False Negative Rate: 0.004

 confusion matrix
 [[26437  2551]
  [  118 28989]]
```

<br><br><br><br>
-------------------------------

## Accuracy of Each Feature
![Single Feature Accuracy](/images/single_feature_accuracy.png)

<br><br><br><br>
-------------------------------

## False Negative Rate of Each Feature
![Single Feature Accuracy](/images/single_feature_false_negative.png)

<br><br><br><br>
-------------------------------

# Bringing this into the world
- Currently not very useful or meaningful
  - should really use combinations of at least 2 features
- How well can `derived features` be discerned in real time?
  - How few computed features do you need to make a good guess
  - What is the computation cost on the derivation of any given feature in real time
- What is the cost of false negatives?
  - If your home router is compromised
  - Equihacks?

<br><br><br><br>
-------------------------------

# What I Scrapped
- Attempted to apply lasso, with little success
  - Instead incorporated `l1` into `LogisticRegression(penalty='l1')`
- Built a pipeline, scrapped it in favor of utilities that call each other
  - Tried crossval, but decided to get a working model first, ran out of time

<br><br><br><br>
-------------------------------

# What I would like to add
- Modeling
  - Run the model on the actual test data
  - Train models on the other attack categories
  - pass in kNN model maybe?
  - Run Combinations on the features
- Real World
  - Cost matrix for the theoretical ramifications of False Negatives
  - Incorporate data related to computational cost for features derived in real time
  - Work with current data set of attacks

<br><br><br><br>
-------------------------------

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
