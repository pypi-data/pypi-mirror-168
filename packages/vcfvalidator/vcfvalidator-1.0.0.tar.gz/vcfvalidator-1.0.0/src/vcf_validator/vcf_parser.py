import gzip
import logging
import sys
import time
import re
from resources import *
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer
import tkinter as tk  
from tkinter import filedialog as fd 


'''

The parser class which parses the VCF attributes with respect to the paper: https://f1000research.com/articles/11-231


'''
      

class vcf_parser:
    
    VCF_METADATA = ["contig", "fileDate", "bioinformatics_source", "reference_url", "reference_ac", "fileformat", "SAMPLE", "INFO"]
    VCF_HEADER = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"]
    
    VCF_REGEX_METADATA = {
    "INFO": "#+INFO=<[a-zA-Z={\D\s\d},]+>",
    "filter": "#+FILTER=<[a-zA-Z={\D\s\d},]+>",
    "format": "#+FORMAT=<[a-zA-Z={\D\s\d},]+>",
    "contig": "#+contig=<[a-zA-Z={\D\s\d},]+>",
    "fileformat": "^#+fileformat=VCFv[0-9.]+",
    "fileDate": "^#+fileDate=(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])",
    "bioinformatics_source": "#+bioinformatics_source=\"([a-zA-z0-9.\d\D\/])+\"" ,
    "reference_url": "#+reference_url=\"([a-zA-z0-9.\d\D\/])+\"",
    "reference_ac": "#+reference_ac=[a-zA-Z\S\d]+",
    "SAMPLE":"^(#+SAMPLE=<[a-zA-Z={\D\s\d},]+>)$"}
    
    VCF_REGEX_HEADER = {"CHROM": "#CHROM\\t\D"}
    
    def __init__(self):
        logging.basicConfig(filename="logs.log",
                    filemode="w",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    force=True)
        logging.captureWarnings(True)
        print ("Parsing VCF file ...")
    
    
    def select_file(self):
        root = tk.Tk()
        root.title("Select the file")
        root.resizable(False, False)
        root.geometry("300x150")
        file = fd.askopenfilename(
                    title="Select a Gziped VCF file",
                    initialdir="/")
        root.destroy()
        return file
    
    '''

    The methond parse_as_chunks requires checking argument (metadata 'm', header data 'h'), chunk_size, 
    and flag to limit the reading till header data only (True for limiting, False for reading complete file) 


    '''
    
    def parse_as_chunks (self, arg, chunk_size, limit_to_header):
        
        filename = self.select_file()
        with gzip.open(filename,"r") as file:
            if arg == "m":
                self.parsing_file(self.VCF_METADATA, self.VCF_REGEX_METADATA, file, arg, chunk_size, limit_to_header)       
            elif arg == "h":
                self.parsing_file(self.VCF_HEADER, self.VCF_REGEX_HEADER, file, arg, chunk_size, limit_to_header)
    

        
    def parsing_file(self, attributes, regex_dict, file, arg, chunk_size, limit_to_header):
        chunk = 1
        line_no = 0
        row_no = 0
        
        print ("Reading chunk no: ", chunk)
        for row in file:
            if not row:
                break
                
            if row_no < chunk_size:
                line_no = line_no + 1   
                row_no = row_no + 1
                line = row.decode("utf-8")
              
                for key, value in regex_dict.items():
                    if (arg == "m" and re.match(value, line) and key in attributes):
                        attributes.remove(key)
                    
                    elif (arg == "h" and re.match(value, line)):
                        header_attributes = line.split("\t")
                        for attribute in header_attributes[0:10]:
                            con_attribute = attribute.replace("#", "")
                            if (con_attribute in attributes):
                                attributes.remove(con_attribute)
                    
                   
                self.check_with_whitespaces(line_no, line)
                if (line.startswith("#CHROM") and limit_to_header == True):
                    break
                        
            else:
                chunk = chunk + 1
                print ("Reading chunk no: ", chunk)
                row_no = 1
                continue
                
            
            
        for attribute in attributes:
            logging.warning("{} not found in the file".format(attribute))
 
    '''

    The methond check_with_whitespaces checks if the data line contains whitespaces or not


    '''
        
    def check_with_whitespaces(self, line_no, line):
        match = re.match("[\\\h]+", line) #checks for whitespaces
        if match:
            logging.info ("  Line : " + str(line_no)  + " have whitespaces")
        else:
            logging.info ("  Line : " + str(line_no) + " does not have whitespaces except new line")
            
            
            