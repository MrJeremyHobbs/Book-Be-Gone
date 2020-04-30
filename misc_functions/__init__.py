import grequests
import requests

def get_xmls(urls):
    rs = (grequests.get(u) for u in urls)
    r = grequests.map(rs)
    
    r_array = []
    for x in r:
        print(x.status_code)
        r_array.append(x)
    
    return r_array
    
def check_bibs_api_GET(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/test?apikey={apikey}'
    r = requests.get(url)
    
    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"BIBS API READ: \t{test_results}"
    
def check_bibs_api_POST(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/test?apikey={apikey}'
    xml = ""
    headers = {'Content-Type': 'application/xml', 'charset':'UTF-8'}
    r       = requests.post(url, data=xml.encode('utf-8'), headers=headers)

    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"BIBS API WRITE:\t{test_results}"

def check_acquisitions_api_GET(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/test?apikey={apikey}'
    r = requests.get(url)
    
    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"ACQ API READ:\t{test_results}"
    
def check_acquisitions_api_POST(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/test?apikey={apikey}'
    xml = ""
    headers = {'Content-Type': 'application/xml', 'charset':'UTF-8'}
    r       = requests.post(url, data=xml.encode('utf-8'), headers=headers)
    
    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"ACQ API WRITE:\t{test_results}"

def check_analytics_api(apikey):
    pass
    
def check_configuration_api_GET(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/test?apikey={apikey}'
    r = requests.get(url)
    
    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"CONF API READ:\t{test_results}"
    
def check_configuration_api_POST(apikey):
    url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/test?apikey={apikey}'
    xml = ""
    headers = {'Content-Type': 'application/xml', 'charset':'UTF-8'}
    r       = requests.post(url, data=xml.encode('utf-8'), headers=headers)
    
    test_results = r.text
    test_results = test_results.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
    test_results = test_results.replace('<test>', '')
    test_results = test_results.replace('</test>', '')
    
    return f"CONF API WRITE:\t{test_results}"