# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging
import conf.config as config
logger = config.globalLogger(logging.DEBUG)
import requests
import json
# import time
from pprint import pformat
from coordinate_distance import haversine


def pullingJson(request_type, station=None):
    base_url = "http://appservices.citibikenyc.com/"
    pullingJson.update_url = base_url + "data2/stations.php?updateOnly=true"
    pullingJson.station_url = base_url + "data2/stations.php"
    pullingJson.helmetsURL = base_url + 'v1/helmet/list'
    pullingJson.branchesURL = base_url + 'v1/branch/list'
    try:
        if request_type == "station":
            r = requests.get(pullingJson.station_url)
            station_dict = json.loads(r.text)
            return_dict = processStation(station_dict)
            json_text = json.dumps(return_dict)
        elif request_type == "update":
            r = requests.get(pullingJson.update_url)
            update_dict = json.loads(r.text)
            diff_dict, return_dict = pullDiffs(update_dict, station)
            # return_dict = processUpdate(update_dict, station)
            logger.info(diff_dict)
            json_text = json.dumps(return_dict)
        else:
            json_text = json.dumps({
                "ok": False,
                "error": "option not recognized"
            })
    except Exception as error:
        logger.exception("/033[31mmoo...")
        json_text = json.dumps({"ok": False, "error": str(error)})
    return json_text


def pullDiffs(update_dict, station_dict):
    diff_dict = {}
    updated_station_dict = {
        "type": "FeatureCollection",
        # "features": [g.values() for g in station_dict['features']]
        "features": [],
        "lastUpdate":  update_dict['lastUpdate']
    }
    for station in update_dict["results"]:
        _id = station['id']
        if int(_id) in station_dict.keys() and station["status"] == "Active":
            # logger.info("%s and %s" %
            #    (station["availableBikes"],\
            # station_dict[_id]['availableBikes']))
            if station["availableBikes"] != station_dict[_id]['availableBikes']:
                # logger.info("we got one!")
                bike_increase = station["availableBikes"] -\
                    station_dict[_id]['availableBikes']
                diff_dict[_id] = bike_increase
            updated_station = station_dict[_id]
            updated_station["availableBikes"] = station["availableBikes"]
            updated_station["availableBikes"] = station["availableBikes"]
            updated_station["availableBikes"] = station["availableBikes"]
            updated_station_dict['features'] += [updated_station]
    # logger.info(updated_station_dict)
    return diff_dict, updated_station_dict


# def processUpdate(update_dict, station_dict):
#     return_dict = {}
#     for station in update_dict["results"]:
#         _id = station['id']
#         if _id in station_dict.keys():
#             if station["availableBikes"] != station_dict[_id]['availableBikes']:
#                 bike_increase = station["availableBikes"] -\
#                    station_dict[_id]['availableBikes']
#         return_dict[_id] = bike_increase
#     return return_dict


def processStation(station_dict):
    station_dict["features"] = range(len(station_dict["results"]))
    return_dict = {"type": "FeatureCollection"}
    del_list = []
    for station_no in range(len(station_dict['results'])):
        station = station_dict["results"][station_no]
        if station['status'] == "Active":
            # station_dict["results"][station_no]['geometry'] = appendGeoJson(station["latitude"], station["longitude"])
            # station_dict["results"][station_no]['type'] = "Feature"
            station['geometry'] = appendGeoJson(station["latitude"], station["longitude"])
            station['type'] = "Feature"
            station_dict["features"][station_no] = station
        else:
            del_list += [station_dict["features"][station_no]]
    return_dict["features"] = station_dict["features"]
    # logger.info(del_list)
    for x in del_list:
        station_dict["features"].remove(x)
    return return_dict


def stationDistanceTiers(station_dict):
    station_id_list = [g["id"] for g in station_dict['results']]
    # for station in station_dict:
    #do some badass distance tiers for each station
    """then add a way to take the stations which see
    a change and explain where the bikes went        """


def appendGeoJson(lat, lng):
    geo = {
        "type": "Point",
        "coordinates": [lng, lat],
        "properties": {"prop0": "value0"}
    }
    return geo


def writeStations():
    station_json = pullingJson("station")
    with open("data/station.json", "w") as open_json:
        open_json.writelines(station_json)


@config.Timeit()
def main():
    # a = True
    for x in range(1):
        json_output = pullingJson("update")
        # print json_output
        logger.debug(pformat(json.loads(json_output)))
        # time.sleep(10)

    # writeStations()

if (__name__ == '__main__'):
    main()
