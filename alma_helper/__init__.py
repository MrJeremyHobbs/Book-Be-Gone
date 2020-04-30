import requests
import xmltodict
import xml.etree.ElementTree as ET
import re

# classes #####################################################################

class item_record:
    def __init__(self, barcode, apikey):
        self.item_record = item_record
        
        self.r = requests.get("https://api-na.hosted.exlibrisgroup.com/almaws/v1/items?view=label&item_barcode="+barcode+"&apikey="+apikey)
        self.xml = self.r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True
        
            # bib_data
            self.mms_id                       = self.dict['item']['bib_data'].get('mms_id', '')
            self.title                        = self.dict['item']['bib_data'].get('title', '')
            self.title_short                  = self.title[:60]
            self.author                       = self.dict['item']['bib_data'].get('author', '')
            self.author_short                 = 'not yet implemented'
            self.network_numbers              = self.dict['item']['bib_data'].get('network_numbers', '')
            self.place_of_publication         = self.dict['item']['bib_data'].get('place_of_publication', '')
            self.publisher_const              = self.dict['item']['bib_data'].get('publisher_const', '')
            
            # holding_data
            self.holding_id                   = self.dict['item']['holding_data'].get('holding_id', '')
            self.call_number_type             = self.dict['item']['holding_data'].get('call_number_type', '')
            self.call_number                  = self.dict['item']['holding_data'].get('call_number', '')
            self.accession_number             = self.dict['item']['holding_data'].get('accession_number', '')
            self.copy_id                      = self.dict['item']['holding_data'].get('copy_id', '')
            self.in_temp_location             = self.dict['item']['holding_data'].get('in_temp_location', '')
            self.temp_library                 = self.dict['item']['holding_data'].get('temp_library', '')
            self.temp_location                = self.dict['item']['holding_data'].get('temp_location', '')
            self.temp_call_number_type        = self.dict['item']['holding_data'].get('temp_call_number_type', '')
            self.temp_call_number             = self.dict['item']['holding_data'].get('temp_call_number', '')
            self.temp_policy                  = self.dict['item']['holding_data'].get('temp_policy', '')
            
            # item_data
            self.pid                          = self.dict['item']['item_data'].get('pid', '')
            self.barcode                      = self.dict['item']['item_data'].get('barcode', '')
            self.creation_date                = self.dict['item']['item_data'].get('creation_date', '')
            self.modification_date            = self.dict['item']['item_data'].get('modification_date', '')
            self.base_status                  = self.dict['item']['item_data'].get('base_status', '')
            self.physical_material_type       = self.dict['item']['item_data'].get('physical_material_type', '')
            self.policy                       = self.dict['item']['item_data'].get('policy', '')
            self.provenance                   = self.dict['item']['item_data'].get('provenance', '')
            self.po_line                      = self.dict['item']['item_data'].get('po_line', '')
            self.is_magnetic                  = self.dict['item']['item_data'].get('is_magnetic', '')
            self.arrival_date                 = self.dict['item']['item_data'].get('arrival_date', '')
            self.year_of_issue                = self.dict['item']['item_data'].get('year_of_issue', '')
            self.enumeration_a                = self.dict['item']['item_data'].get('enumeration_a', '')
            self.chronology_i                 = self.dict['item']['item_data'].get('chronology_i', '')
            self.description                  = self.dict['item']['item_data'].get('description', '_blank')
            self.receiving_operator           = self.dict['item']['item_data'].get('receiving_operator', '')
            self.process_type                 = self.dict['item']['item_data'].get('process_type', '')
            self.library                      = self.dict['item']['item_data'].get('library', '')
            
            self.location_dict                = self.dict['item']['item_data'].get('location', '')
            self.location_long                = self.location_dict.get('@desc', '')
            self.location_short               = self.location_dict.get('#text', '')
            
            self.alternative_call_number      = self.dict['item']['item_data'].get('alternative_call_number', '')
            self.alternative_call_number_type = self.dict['item']['item_data'].get('alternative_call_number_type', '')
            self.storage_location_id          = self.dict['item']['item_data'].get('storage_location_id', '')
            self.pages                        = self.dict['item']['item_data'].get('pages', '')
            self.pieces                       = self.dict['item']['item_data'].get('pieces', '')
            self.public_note                  = self.dict['item']['item_data'].get('public_note', '')
            self.fulfillment_note             = self.dict['item']['item_data'].get('fulfillment_note', '')
            
            self.internal_note_1              = self.dict['item']['item_data'].get('internal_note_1', '')
            self.internal_note_2              = self.dict['item']['item_data'].get('internal_note_2', '')
            self.internal_note_3              = self.dict['item']['item_data'].get('internal_note_3', '')
            
            self.statistics_note_1            = self.dict['item']['item_data'].get('statistics_note_1', '')
            self.statistics_note_2            = self.dict['item']['item_data'].get('statistics_note_2', '')
            self.statistics_note_3            = self.dict['item']['item_data'].get('statistics_note_3', '')
            
            self.requested                    = self.dict['item']['item_data'].get('requested', '')
            self.enumeration_a                = self.dict['item']['item_data'].get('enumeration_a', '')
            self.enumeration_b                = self.dict['item']['item_data'].get('enumeration_b', '')
            self.enumeration_c                = self.dict['item']['item_data'].get('enumeration_c', '')
            self.enumeration_d                = self.dict['item']['item_data'].get('enumeration_d', '')
            self.enumeration_e                = self.dict['item']['item_data'].get('enumeration_e', '')
            self.enumeration_f                = self.dict['item']['item_data'].get('enumeration_f', '')
            self.enumeration_g                = self.dict['item']['item_data'].get('enumeration_g', '')
            self.enumeration_h                = self.dict['item']['item_data'].get('enumeration_h', '')
            self.enumeration_i                = self.dict['item']['item_data'].get('enumeration_i', '')
            self.enumeration_j                = self.dict['item']['item_data'].get('enumeration_j', '')
            self.enumeration_k                = self.dict['item']['item_data'].get('enumeration_k', '')
            self.enumeration_l                = self.dict['item']['item_data'].get('enumeration_l', '')
            self.enumeration_m                = self.dict['item']['item_data'].get('enumeration_m', '')
            
            #self.parsed_call_number           = self.dict['item']['item_data']['parsed_call_number'].get('call_no', '')
            
            # description
            if self.description == None:
                self.description = ""
                

class bib_record:
    def __init__(self, r):
        self.bib_record = bib_record
        
        #self.r = requests.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mms_id}?apikey={apikey}")
        self.r   = r
        self.xml = r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True
        
            # create dict
            self.dict = xmltodict.parse(self.xml)
            
            # bib_data
            self.mms_id                     = self.dict['bib'].get('mms_id')
            self.record_format              = self.dict['bib'].get('record_format')
            self.linked_record_id_type      = self.dict['bib'].get('linked_record_id_type')
            self.title                      = self.dict['bib'].get('title')
            self.author                     = self.dict['bib'].get('author')
            self.isbn                       = self.dict['bib'].get('isbn')
            self.place_of_publication       = self.dict['bib'].get('place_of_publication')
            self.publisher_const            = self.dict['bib'].get('publisher_const')
            self.created_by                 = self.dict['bib'].get('created_by')
            self.created_date               = self.dict['bib'].get('created_date')
            self.last_modified_by           = self.dict['bib'].get('last_modified_by')
            self.last_modified_date         = self.dict['bib'].get('last_modified_date')
            self.suppress_from_publishing   = self.dict['bib'].get('suppress_from_publishing')
            self.originating_system         = self.dict['bib'].get('originating_system')
            self.originating_system_id      = self.dict['bib'].get('originating_system_id')
            self.leader                     = self.dict['bib']['record'].get('leader')
            
            # oclc numbers
            self.network_numbers_dict       = self.dict['bib'].get('network_numbers')
            self.has_oclc_number            = False
            
            try:
                self.network_numbers        = self.network_numbers_dict['network_number']
                self.has_oclc_number        = True
            except:
                self.network_numbers        = []
                self.has_oclc_number        = False
            
            # bib level
            self.level = 'unknown' # default value
            
            leader_slice = (self.leader[7])
            if leader_slice == 'm': self.level = 'book'
            if leader_slice == 's': self.level = 'serial'
    
    def get_primary_oclc_number(self, oclc_prefixes):
        for n in self.network_numbers:
            for prefix in oclc_prefixes:
                if prefix in n:
                    regex = r"[0-9]+"
                    match = re.search(regex, n)
                    primary_oclc_number = match.group(0)
                    return primary_oclc_number
        return None

    def search(self, search_phrase):
        regex   = re.compile(search_phrase, re.IGNORECASE)
        search = regex.search(self.xml)
        if search != None:
            return 'found'
        else:
            return 'not found'
 
 
class items_record:
    def __init__(self, r):
        self.items_record = items_record
        
        #self.r = requests.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mms_id}/holdings/{holding_id}/items?limit=10&offset=0&apikey={apikey}")
        self.r   = r
        self.xml = r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True
        
            # parse
            self.total_record_count = int(self.dict['items']['@total_record_count'])

        
class holdings_record:
    def __init__(self, r):
        self.holdings_record = holdings_record

        #self.r = requests.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mms_id}/holdings?apikey={apikey}")
        self.r   = r
        self.xml = r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True
        
            # parse
            self.total_record_count = int(self.dict['holdings']['@total_record_count'])
        
        
class po_lines_record:
    def __init__(self, r):
        self.po_lines_record = po_lines_record

        #self.r = requests.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines?q=mms_id~{mms_id}&status=ALL_WITH_CLOSED&limit=10&offset=0&order_by=title&direction=desc&acquisition_method=ALL&apikey={apikey}")
        self.r   = r
        self.xml = r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True
        
            # parse
            self.total_record_count = int(self.dict['po_lines']['@total_record_count'])
        
class add_to_set:
    def __init__(self, set_id, mms_id, holding_id, item_pid, barcode, apikey):
        self.set = set
        
        self.set_xml = \
    f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<set link="https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{set_id}">
  <id>{set_id}</id>
  <number_of_members link="https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{set_id}/members">1</number_of_members>
<members total_record_count="1">
  <member link="https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}">
    <id>{item_pid}</id>
    <description>{barcode}</description>
  </member>
</members>
</set>'''

        self.url     = f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{set_id}?op=add_members&apikey={apikey}"
        self.headers = {'Content-Type': 'application/xml', 'charset':'UTF-8'}
        self.r       = requests.post(self.url, data=self.set_xml.encode('utf-8'), headers=self.headers)
        
        self.xml = self.r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.successful = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.successful = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.successful = True
            
            
class add_note_to_item:
    def __init__(self, item_xml, item_note_field, item_wd_note, mms_id, holding_id, item_pid, apikey):
        self.add_note_to_item = add_note_to_item
        
        # update item with note
        item                = ET.fromstring(item_xml)
        item_stat_note      = item.find(f'item_data/{item_note_field}')
        item_stat_note.text = item_wd_note
        item_final_xml      = ET.tostring(item, encoding="unicode", method="xml")
        
        
        self.url     = f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}?apikey={apikey}"
        self.headers = {'Content-Type': 'application/xml', 'charset':'UTF-8'}
        self.r       = requests.put(self.url, data=item_final_xml.encode('utf-8'), headers=self.headers)
        
        self.xml = self.r.text
        
        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.successful = False
            self.error_msg = "Invalid API Key."
            return
        
        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)
        
        if self.r.status_code != 200:
            self.successful = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.successful = True