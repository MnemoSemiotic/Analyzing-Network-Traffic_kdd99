# analyzing-network-traffic_kdd99
Tovio Roberts - Galvanize Data Science Analytics capstone

### 3 Questions:
1. Is it possible to predict the label (attack name or normal) of the entry without knowing the protocol?
2. Can the 0-heavy features be dropped?
3. What features should be dummy-ized?

Attacks fall into these 4 main categories:
- DOS: denial-of-service, e.g. syn flood;
- R2L: unauthorized access from a remote machine, e.g. guessing password;
- U2R:  unauthorized access to local superuser (root) privileges, e.g., various ``buffer overflow'' attacks;
- probing: surveillance and other probing, e.g., port scanning.

#### Features in the raw dataset
| Column Name  | Type of Data  | Description      |
|-----------|----------------------------------------|------------------|
|duration                     |int64     | length in seconds of the connection|
|protocol_type                |object    | the connection protocol |
|service                      |object    |
|flag                         |object    |
|src_bytes                    |int64     |
|dst_bytes                    |int64     |
|land                         |int64     |
|wrong_fragment               |int64     |
|urgent                       |int64     |
|hot                          |int64     |
|num_failed_logins            |int64     |
|logged_in                    |int64     |
|num_compromised              |int64     |
|root_shell                   |int64     |
|su_attempted                 |int64     |
|num_root                     |int64     |
|num_file_creations           |int64     |
|num_shells                   |int64     |
|num_access_files             |int64     |
|num_outbound_cmds            |int64     |
|is_host_login                |int64     |
|is_guest_login               |int64     |
|count                        |int64     |
|srv_count                    |int64     |
|serror_rate                  |float64   |
|srv_serror_rate              |float64   |
|rerror_rate                  |float64   |
|srv_rerror_rate              |float64   |
|same_srv_rate                |float64   |
|diff_srv_rate                |float64   |
|srv_diff_host_rate           |float64   |
|dst_host_count               |int64     |
|dst_host_srv_count           |int64     |
|dst_host_same_srv_rate       |float64   |
|dst_host_diff_srv_rate       |float64   |
|dst_host_same_src_port_rate  |float64   |
|dst_host_srv_diff_host_rate  |float64   |
|dst_host_serror_rate         |float64   |
|dst_host_srv_serror_rate     |float64   |
|dst_host_rerror_rate         |float64   |
|dst_host_srv_rerror_rate     |float64   |
|label                        |object    |
