#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    all_docs = nginx.count_documents({})

    print("{} logs".format(all_docs))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status = nginx.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

    print("IPs:")
    ips = nginx.aggregate([
        {"$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}},
        {"$sort": {"totalRequests": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        ip_num = ip["_id"]
        ip_count = ip["totalRequests"]
        print("\t{}: {}".format(ip_num, ip_count))
