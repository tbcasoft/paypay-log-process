from collections import defaultdict
import json
from response_pairs import get_response
import ultraimport # type: ignore

get_time = ultraimport('__dir__/../generate_time.py', 'get_time')
get_cookie = ultraimport('__dir__/../tc_login.py', 'get_cookie')


data_collector = {
    "count" : defaultdict(dict),
    "destAmount" : defaultdict(dict)
}

start_time, end_time = get_time()
cookie = get_cookie()
response = get_response(cookie, start_time, end_time)
# print(json.dumps(response, indent=4))

buckets = response["aggregations"]["7"]["buckets"][0]

count = data_collector["count"]
dest_amount = data_collector["destAmount"]

count["total"] = buckets["doc_count"]
cpm = buckets["13"]["buckets"][0]["8"]["buckets"][0]["9"]["buckets"]
mpm = buckets["13"]["buckets"][1]["8"]["buckets"][0]["9"]["buckets"]


def getCount(source_dict, target_dir):
    target_dir[source_dict["key"]] = defaultdict(dict)
    target_dir[source_dict["key"]] = source_dict["doc_count"]


def getDestAmount(source, target_dir):
    issuer = source["key"]
    target_dir[issuer] = defaultdict(dict)
    source = source["5"]["buckets"][0]["12"]["buckets"][0]["6"]["buckets"][0]["4"]["buckets"][0]["3"]
    dest_amount_val = source["value"]
    target_dir[issuer] = int(dest_amount_val)



for i in range(len(cpm)):
    getCount(cpm[i], count["CPM"])
    getCount(mpm[i], count["MPM"])
    getDestAmount(cpm[i], dest_amount["CPM"])
    getDestAmount(mpm[i], dest_amount["MPM"])


print(json.dumps(data_collector, indent=4))
# # print(json.dumps(buckets, indent=4))
# print(json.dumps(cpm, indent=4))
# print(json.dumps(mpm, indent=4))