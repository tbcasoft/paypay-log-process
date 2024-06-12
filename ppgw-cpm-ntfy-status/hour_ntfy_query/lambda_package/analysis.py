from collections import defaultdict
from datetime import datetime
import json
from hour import set_time

from mainnet_query import get_query

start_time, end_time = set_time()

# This is for manual configuring specific time frame for testing purposes
test_start, test_end = "2024-05-30T10:21:00.000Z", "2024-05-30T10:30:00.000Z"
start_time, end_time = int(datetime.fromisoformat(test_start).timestamp()), int(datetime.fromisoformat(test_end).timestamp())
get_query(start_time, end_time)

def result_analysis(event_streams):

    non_unique = defaultdict(int)
    unique = defaultdict(int) 
    seen_qr = set()

    for id in event_streams.keys():

        event_stream = event_streams[id]
        qr = event_stream["qr"]
        result_code = event_stream["result"]
        result_key = ""
        match result_code:
            case "SUCCESS" | "MERCHANT_SUSPENDED" | "HIVEX_UNAVAILABLE_MERCHANT":
                result_key = result_code
            case "INVALID_CODE":
                if "28180104" in qr:
                    result_key = "Dynamic_QR"
                elif "p2p01" in qr:
                    result_key = "P2P"
                else:
                    result_key = "Others"
        non_unique[result_key] += 1
        unique[result_key] += 0 if qr in seen_qr else 1
        print(qr, "(unique)" if qr not in seen_qr else "(repeat)", "\n")
        seen_qr.add(qr)

    non_unique["Total"] = sum(non_unique.values())
    unique["Total"] = sum(unique.values())
    print("non-unique analysis:", json.dumps(non_unique, indent=4))
    print("unique analysis:", json.dumps(unique, indent=4))
    return non_unique, unique



# For testing
test_start, test_end = "2024-05-29T09:05:00.000Z", "2024-05-29T10:06:00.000Z"
start_time, end_time = int(datetime.fromisoformat(test_start).timestamp()), int(datetime.fromisoformat(test_end).timestamp())

get_query(start_time, end_time)