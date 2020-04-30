#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import os
import sys

# local modules
import bbg_config as config
from misc_functions import *
import alma_helper as alma

# main program ################################################################
def main(*args):
    # barcode
    barcode = gui.get_barcode()
    if barcode == "":
        messagebox.showerror("Error", "Bad barcode.")
        gui.update_status_failure(barcode, "Bad barcode.")
        return
    gui.clear_barcode()
    
    item = alma.item_record(barcode, config.apikey)
    
    if item.found == False:
        messagebox.showerror("Error", item.error_msg)
        gui.update_status_failure(barcode, item.error_msg)
        return
    
    # get other records using async
    urls = [
        f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{item.mms_id}?apikey={config.apikey}",
        f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{item.mms_id}/holdings?apikey={config.apikey}",
        f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{item.mms_id}/holdings/{item.holding_id}/items?limit=10&offset=0&apikey={config.apikey}",
        f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines?q=mms_id~{item.mms_id}&status=ALL_WITH_CLOSED&limit=10&offset=0&order_by=title&direction=desc&acquisition_method=ALL&apikey={config.apikey}"
    ]
    (bib_r, holdings_r, items_r, po_lines_r) = get_xmls(urls)
    
    bib = alma.bib_record(bib_r)
    holdings = alma.holdings_record(holdings_r)
    items = alma.items_record(items_r)
    po_lines = alma.po_lines_record(po_lines_r)
    
    # check if objects initiated successfully
    record_list = [bib, holdings, items, po_lines]
    for record in record_list:
        if record.found == False:
            messagebox.showerror('Exception', 'RECORD NOT FOUND')
            gui.update_status_failure(item.title_short, 'EXCEPTION - RECORD NOT FOUND')
            return
    
    # serial check
    if config.serial_check == 'active':
        if bib.level == 'serial':
            messagebox.showerror('Exception', 'EXCEPTION - SERIAL')
            gui.update_status_failure(item.title_short, 'EXCEPTION - SERIAL')
            return
            
    # other items check
    if config.other_items_check  == 'active':
        if items.total_record_count > 1:
            messagebox.showerror('Exception', 'EXCEPTION - OTHER ITEMS FOUND')
            gui.update_status_failure(item.title_short, 'EXCEPTION - OTHER ITEMS FOUND')
            return
            
    # other holdings check
    if config.other_holdings_check  == 'active':
        if holdings.total_record_count > 1:
            messagebox.showerror('Exception', 'EXCEPTION - OTHER HOLDINGS FOUND')
            gui.update_status_failure(item.title_short, 'EXCEPTION - OTHER HOLDINGS FOUND')
            return
            
    # attached orders check
    if config.attached_orders_check  == 'active':
        if po_lines.total_record_count > 0:
            messagebox.showerror('Exception', 'EXCEPTION - PO LINES FOUND')
            gui.update_status_failure(item.title_short, 'EXCEPTION - PO LINES FOUND')
            return
            
    # bib search
    if config.bib_search  == 'active':
        bib_search = bib.search(config.bib_search_phrase)
        if bib_search == 'found':
            messagebox.showerror('Exception', f'EXCEPTION - FOUND KEYWORDS IN BIB ("{config.bib_search_phrase}")')
            gui.update_status_failure(item.title_short, f'EXCEPTION - FOUND KEYWORDS IN BIB ("{config.bib_search_phrase}")')
            return
    
    # add note to item record
    if config.add_item_note == 'active':
        add_item_note = alma.add_note_to_item(item.xml, config.item_note_field, config.item_wd_note, item.mms_id, item.holding_id, item.pid, config.apikey)
        
        # check if successful
        if add_item_note.successful == False:
            messagebox.showerror("Error", add_item_note.error_msg)
            gui.update_status_failure(item.title, f'PROBLEM WRITING WD NOTE IN ITEM RECORD - {add_item_note.error_msg}"')
            return
        
    # add to set
    if config.add_to_set == 'active':
        add_to_set = alma.add_to_set(config.wd_set_id, item.mms_id, item.holding_id, item.pid, barcode, config.apikey)
        
        # check if successful
        if add_to_set.successful == False:
            messagebox.showerror("Error", add_to_set.error_msg)
            gui.update_status_failure(item.title, f'PROBLEM ADDING ITEM TO SET - "{add_to_set.error_msg}"')
            return
    
    # add to oclc log file
    primary_oclc_number = bib.get_primary_oclc_number(config.oclc_prefixes)
    if (config.oclc_logging         == 'active' and \
        primary_oclc_number         != None     and \
        holdings.total_record_count == 1        and \
        items.total_record_count    == 1):
        
        # write to file
        with open(config.oclc_log_path, "a") as oclc_log_file:
           oclc_log_file.write(f"{primary_oclc_number}\n")
        oclc_log_file.close
    
    # finish
    gui.update_status_success(item.title_short)

# functions ###################################################################
def check_apikeys():
    r1 = check_bibs_api_GET(config.apikey)
    r2 = check_bibs_api_POST(config.apikey)
    r3 = check_acquisitions_api_GET(config.apikey)
    r4 = check_configuration_api_GET(config.apikey)
    r5 = check_configuration_api_POST(config.apikey)
    
    test_results     = "\n-----------------------------------\n".join([r1, r2, r3, r4, r5])
    test_results_msg = \
    f"API Test Results\n--------------------\n\
(Press CTRL+C to copy this message to the clipboard.)\n\n\n\
{test_results}"
                        
    messagebox.showinfo("Check APIs", test_results_msg)
    
    
# gui #########################################################################
class gui:
    def __init__(self, master):
        self.master = master
        master.title(f"Book-Be-Gone {version}")
        master.resizable(0, 0)
        master.minsize(width=600, height=100)
        master.iconbitmap(".\images\logo_small.ico")

        logo_image = PhotoImage(file=".\images\logo_large.png")
        self.logo = Label(image=logo_image)
        self.logo.image = logo_image
        self.logo.pack()

        self.status_title = Label(height=1, text="Scan barcode to begin.", font="Consolas 12 italic")
        self.status_title.pack(fill="both", side="top")

        self.status_wd = Label(height=1, text="READY", font="Consolas 12 bold", fg="green")
        self.status_wd.pack(fill="both", side="top")

        self.barcode_entry_field = Entry(font="Consolas 16")
        self.barcode_entry_field.focus()
        self.barcode_entry_field.bind('<Key-Return>', main)
        self.barcode_entry_field.pack(fill="both", side="top")
        
        self.scan_button = Button(text="SCAN", font="Arial 16", command=main)
        self.scan_button.pack(fill="both", side="top")
        
        # menus
        self.menubar = Menu(root)
        
        self.file_menu = Menu(self.menubar, tearoff = 0)
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label = "File", menu=self.file_menu)
        
        self.settings_menu = Menu(self.menubar, tearoff = 0)
        self.settings_menu.add_command(label = "Test API keys (takes a minute)", command = check_apikeys)
        self.menubar.add_cascade(label = "Settings", menu=self.settings_menu)
        
        root.config(menu=self.menubar)
        
    def get_barcode(self):
        barcode = self.barcode_entry_field.get()
        barcode = barcode.replace(" ", "")
        barcode.rstrip("\r\n")
        return barcode
        
    def clear_barcode(self):
        self.barcode_entry_field.delete(0, END)
        self.status_title.config(text="")
        self.status_wd.config(text="")
        
    def update_status_success(self, title):
        self.status_title.config(text=title)
        self.status_wd.config(text="SUCCESSFULLY ADDED TO SET", fg="green")
        
    def update_status_failure(self, title, msg):
        self.status_title.config(text=title)
        self.status_wd.config(text=msg, fg="red")
    
        
# toplevel ####################################################################
version = '3.1'    
    
# load gui
root = Tk()
gui = gui(root)

# load and check configurations
config = config.load_configuration('config.ini')
if config.errors:
    config_errors = "\n\n".join(config.errors)
    messagebox.showerror("Errors Found!", 
                        f"ERRORS FOUND IN CONFIG.INI:\n" \
                        "----------------------------------------\n\n" \
                        "{config_errors}")
    sys.exit()

root.mainloop()