# how to run this file: python scarp2.py 779608863132 | python -m json.tool > html
# -*- coding: utf-8 -*-
import requests

# If you want to follow multiple packages:
# http://wwwapps.ups.com/etracking/tracking.cgi?InquiryNumber1=YOURNUMBER1&InquiryNumber2=YOURNUMBER2&InquiryNumber3=YOURNUMBER3&track.x=0&track.y=0%22
#https://api.ntag.fr/ups/doc.php
#http://wwwapps.ups.com/etracking/tracking.cgi?track.x=0&track.y=0&InquiryNumber1={YOUR TRACKING NUMBER}
def track_ups(tracking_number):
    r = requests.post("http://api.ntag.fr/ups/?id="+tracking_number)
    return r.content