#!/bin/env/python
import argparse
import json
import sys
import urllib2


def get_rest_response(endpoint):
    try:
        result = json.loads(urllib2.urlopen(endpoint).read())
    except urllib2.URLError:
        print('Error accessing `{}`, please ensure that you have specified '
              'the correct bucket and hostname/IP'.format(endpoint))
        sys.exit(1)
    else:
        return result


def get_bucket_list():
    endpoint = ('http://{}:8091/pools/default/buckets'.format(args.ip))
    bucket_list = get_rest_response(endpoint)
    bucket_list = [bucket['name'] for bucket in bucket_list]
    return bucket_list


def get_stat(stat, bucket):
    endpoint = (
        'http://{}:8091/pools/default/buckets/{}/stats'.format(args.ip,
                                                               bucket))
    stat_dict = get_rest_response(endpoint)
    stat_dict = stat_dict['op']['samples']

    try:
        sample_list = stat_dict[stat]
    except KeyError:
        print('Error - stat {} does not exist in the REST response'
              .format(stat))
        sys.exit(1)
    else:
        # Average last 60 seconds
        value = sum(sample_list) / len(sample_list)
        return value


def main():
    parse_args(sys.argv[1:])

    if args.bucket:
        if isinstance(args.bucket, list):
            buckets = args.bucket
        else:
            buckets = [args.bucket]
    else:
        buckets = get_bucket_list()

    for bucket in buckets:
        value = get_stat(args.stat, bucket)
        print('{} for bucket {} is {}'.format(args.stat, bucket, value))


def parse_args(passed_args):
    parser = argparse.ArgumentParser(description='A tool to summarise stats'
                                     ' for an entire Couchbase cluster without'
                                     ' needing to log into every node')
    parser.add_argument('ip',
                        help='IP of one node in the cluster')
    parser.add_argument('stat', help='Stat that you wish to summarise')
    parser.add_argument('--bucket', '-b',
                        help='Bucket that you wish to get stats for')
    global args
    args = parser.parse_args(passed_args)

if __name__ == '__main__':
    sys.exit(main())



