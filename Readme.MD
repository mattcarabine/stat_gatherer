# Stat Gatherer

A small script to wrap around the Couchbase Server REST API used to retrieve
stats per bucket.

## Usage
Get stats for all buckets:
```
python stat_gatherer.py <node_ip/hostname> <stat_name>
```

Get stats for specific bucket:
```
python stat_gatherer.py <node_ip/hostname> <stat_name> -b <bucket_name>
```

Examples:
```
python stat_gatherer.py localhost curr_items

curr_items for bucket default is 1
curr_items for bucket default2 is 1
curr_items for bucket test is 0
```

```
python stat_gatherer.py localhost curr_items -b default

curr_items for bucket default is 1
```