import os.path
import urllib.request
import pandas as pd
import scirpy as sc
def available_datasets():
    """Prints the available datsets"""

def select_dataset(dataset_name,current_path,update=True):
    func_dict = {"mcpastcr": McPASTCR_dataset,
                 "tenxgenomics_onekcellshealthy":tenx_genomics}

    dataset_load_fx = lambda f,dataset_name,current_path,update: lambda dataset_name,current_path,update: f(dataset_name,current_path,update)

    data_load_function = dataset_load_fx(func_dict[dataset_name],dataset_name,current_path,update)

    data_load_function(dataset_name,current_path,update)
    print("Done")

def vdjdb_dataset(update):
    """https://vdjdb.cdr3.net/"""
    dataset = sc.datasets.vdjdb

def McPASTCR_dataset(dataset_name,current_path,update):
    """http://friedmanlab.weizmann.ac.il/McPAS-TCR/"""
    url_download = "http://friedmanlab.weizmann.ac.il/McPAS-TCR/session/47a5ea892b17bcea9c4a38a9b2a9b141/download/downloadDB?w="
    download_file = "/gleipnir/data/mcpastcr/McPAS-TCR.cvs"
    if not update:
        if os.path.exists(download_file):
            print("File found in the /data folder, reading ...")
        else:
            print("File NOT found in the /data folder, downloading...")
            urllib.request.urlretrieve(url_download, download_file)
            print("Download finished. Reading ...")
    else:
        urllib.request.urlretrieve(url_download, download_file)
        print("Download finished.Reading ...")

    data =pd.read_csv(download_file,sep=",", encoding="windows-1252")
    print(data)


def iebd_dataset():
    """https://www.iedb.org/"""


def imgt_dataset():
    """https://www.imgt.org/"""

def atlas_dataset():
    """https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5860664/"""

def tcrdb_dataset():
    """https://academic.oup.com/nar/article/49/D1/D468/5912818"""

def immnunecode_database():
    """https://immunerace.adaptivebiotech.com/data/
    https://clients.adaptivebiotech.com/pub/covid-2020"""

def tenx_genomics(dataset_name,current_path,update):
    """https://www.10xgenomics.com/resources/datasets/human-b-cells-from-a-healthy-donor-1-k-cells-2-standard-6-0-0"""
    subname = dataset_name.split("_")[-1]
    if subname == "onekcellshealthy":
        print("Analyzing VDJ 1k cells from a healthy donor")

