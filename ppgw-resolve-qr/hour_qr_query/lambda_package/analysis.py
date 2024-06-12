from collections import defaultdict

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
        seen_qr.add(qr)

    non_unique["Total"] = sum(non_unique.values())
    unique["Total"] = sum(unique.values())
    
    return non_unique, unique
