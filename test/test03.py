'''

@author: Zxh
'''
import urllib2
import urllib
import json
import requests

r = requests
url = "http://localhost:8050/"
url_1 = url + 'indoor'
post_data = '''{
	"1": {
		"59": {
			"temperature": "5",
			"humidity": "60",
			"radiation": "500",
			"co2": "400",
			"update_time": "2016-09-19 21:25:50"
		}
	},
	"2": {},
	"3": {},
	"4": {},
	"5": {},
	"6": {},
	"7": {},
	"8": {}
}'''
r.post(url_1, post_data)
# print type(post_data)
# # post_data=json.dumps(post_data)
# # print type(post_data)
# post_data = urllib.quote_plus(post_data)
# req = urllib2.Request(url=url_1, data=post_data)
# print req
# print urllib2.urlopen(req).read()