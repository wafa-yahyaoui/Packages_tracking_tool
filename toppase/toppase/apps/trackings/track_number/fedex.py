import requests
import json


# https://wsbeta.fedex.com:443/web-services/track
def track_fedex(tracking_number):
    data = requests.post('https://www.fedex.com/trackingCal/track', data={
        'data': json.dumps({
            'TrackPackagesRequest': {
                'appType': 'wtrk',
                'uniqueKey': '',
                'processingParameters': {
                    'anonymousTransaction': True,
                    'clientId': 'WTRK',
                    'returnDetailedErrors': True,
                    'returnLocalizedDateTime': True
                },
                'trackingInfoList': [{
                    'trackNumberInfo': {
                        'trackingNumber': str(tracking_number),
                        'trackingQualifier': '',
                        'trackingCarrier': ''
                    }
                }]
            }
        }),
        'action': 'trackpackages',
        'locale': 'us_US',
        'format': 'json',
        'version': 99
    })
    json_filter = {}
    json_filter["scan_event_list"]=[]
    scan_event_list = json.loads(data.content)["TrackPackagesResponse"]["packageList"][0]["scanEventList"]
    for i in range(len(scan_event_list)):
        json_filter["scan_event_list"].append({"status":scan_event_list[i]["status"],"date":scan_event_list[i]["date"],"location":scan_event_list[i]["scanLocation"]})
    estimated_time_delivery = json.loads(data.content)["TrackPackagesResponse"]["packageList"][0]["isEstimatedDeliveryDtLabel"]
    json_filter["estimated_date"] = estimated_time_delivery
    json_filter["shipper"] ="fedex"
    return json.dumps(json_filter)


# track_fedex("723601251970")