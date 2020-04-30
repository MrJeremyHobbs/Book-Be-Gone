import configparser
import os

# configurations ##############################################################
class load_configuration:
    def __init__(self, config_file):
        self.load_configuration = load_configuration
        
        self.errors = []
        
        # check file path
        if os.path.isfile('config.ini') == True:
            self.file_found = True
        else:
            self.errors.append("Can't find config.ini file.")
            self.file_found = False
        
        # load configuration
        if self.file_found == True:
            config = configparser.ConfigParser()
            config.read(config_file)
            
            self.version                    = config['misc'].get('version')
            self.apikey                     = config['misc'].get('apikey')
            
            self.serial_check               = config['checks'].get('serial_check')
            self.other_items_check          = config['checks'].get('other_items_check')
            self.other_holdings_check       = config['checks'].get('other_holdings_check')
            self.attached_orders_check      = config['checks'].get('attached_orders_check')
            self.bib_search                 = config['checks'].get('bib_search')
            self.bib_search_phrase          = config['checks'].get('bib_search_phrase')

            self.add_item_note              = config['add_statistics_note'].get('add_item_note')
            self.item_note_field            = config['add_statistics_note'].get('item_note_field')
            self.item_wd_note               = config['add_statistics_note'].get('item_wd_note')
            
            self.add_to_set                 = config['add_to_set'].get('add_to_set')
            self.wd_set_id                  = config['add_to_set'].get('wd_set_id')
            
            self.oclc_logging               = config['oclc_log'].get('oclc_logging')
            self.oclc_log_path              = config['oclc_log'].get('oclc_log_path').replace('\\', '//')
            self.oclc_prefixes              = config['oclc_log'].get('oclc_prefixes').split(',')
            
            # check for active or inactive status
            if (self.serial_check != 'active') and (self.serial_check != 'inactive'):
                self.errors.append("[serial_check] should be 'active' or 'inactive'.")
                
            if (self.other_items_check != 'active') and (self.other_items_check != 'inactive'):
                self.errors.append("[other_items_check] should be 'active' or 'inactive'.")
            
            if (self.other_holdings_check != 'active') and (self.other_holdings_check != 'inactive'):
                self.errors.append("[other_holdings_check] should be 'active' or 'inactive'.")
                
            if (self.attached_orders_check != 'active') and (self.attached_orders_check != 'inactive'):
                self.errors.append("[attached_orders_check] should be 'active' or 'inactive'.")
                
            if (self.bib_search != 'active') and (self.bib_search != 'inactive'):
                self.errors.append("[bib_search] should be 'active' or 'inactive'.")
                
            if (self.add_item_note != 'active') and (self.add_item_note != 'inactive'):
                self.errors.append("[add_item_note] should be 'active' or 'inactive'.")
            
            if (self.add_to_set != 'active') and (self.add_to_set != 'inactive'):
                self.errors.append("[add_to_set] should be 'active' or 'inactive'.")
                
            if (self.oclc_logging != 'active') and (self.oclc_logging != 'inactive'):
                self.errors.append("[oclc_logging] should be 'active' or 'inactive'.")
            
            # check bib search params
            if self.bib_search == 'active':
                if self.bib_search_phrase == '':
                    self.errors.append("[bib_search_phrase] is blank.")
            
            # check item note params
            if self.add_item_note == 'active':
                if self.item_note_field == "":
                    self.errors.append("[item_note_field] is blank.")
                
                if (self.item_note_field != 'statistics_note_1' and \
                    self.item_note_field != 'statistics_note_2' and \
                    self.item_note_field != 'statistics_note_3') :
                    self.errors.append("[item_note_field] is not a valid field in Alma.\nRecommended: 'statistics_note_1', 'statistics_note_2', 'statistics_note_3'")
                
                if self.item_wd_note == "":
                    self.errors.append("[item_wd_note] is blank.")
                    
            # check add to set params
            if self.add_to_set == 'active':
                if self.wd_set_id == '':
                    self.errors.append("[wd_set_id] is blank.")
            
            # check if log params are correct
            if self.oclc_logging == 'active':
                
                self.relative_log_path = os.path.dirname(self.oclc_log_path)
                if os.path.isdir(self.relative_log_path) == True:
                    self.oclc_log_path_ok = True
                else:
                    self.oclc_log_path_ok = False
                    self.errors.append("[oclc_log_path] not found.")
                    
                if self.oclc_prefixes[0] == "":
                    self.errors.append("[oclc_prefixes] is empty")
            