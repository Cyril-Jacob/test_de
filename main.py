import logging
import sys
from pathlib import Path
from drug_journal.drug import Drug
from drug_journal.pub.publication import Publication
from drug_journal.pub.pubmed import Pubmed
from drug_journal.pub.clinical_trials import ClinicalTrials 
from drug_journal.reader.csv_pub_reader import CSVPubReader
from drug_journal.reader.csv_drug_reader import CSVDrugReader
from drug_journal.reader.json_pub_reader import JSONPubReader


def data_pipeline():

    '''Drug - data loading: reading CSV files'''
    log.debug(f"Reading Drugs csv file")

    drug_r = CSVDrugReader(Path('data\input\drugs.csv'))
    rows = list(drug_r.data_iter())
    log.info(f"Drugs csv file has {len(rows)} rows\n")
   
    
    '''Pubmed - data loading: reading CSV file'''
    
    log.info(f"Reading Pubmed csv file")
    rdr = CSVPubReader(Path('data\input\pubmed.csv'))
    rows = list(rdr.data_iter()) 
    log.info(f"pubmed csv file has {len(rows)} rows\n")

    '''Pubmed - data cleaning: fix or remove inconsistencies'''
    
    log.info(f"Cleaning Pubmed csv file")
    iter = Pubmed.load(rdr.data_iter())
    pubmed_csv_rows = list(iter) 
    log.info(f"pubmed cleaned csv output has {len(pubmed_csv_rows)} rows\n")


    '''Pubmed - data loading: reading JSON file'''
    
    log.info(f"Reading Pubmed json file")    
    rdr = JSONPubReader(Path('data\input\pubmed.json'))
    rows = list(rdr.data_iter()) 
    log.info(f"pubmed json file has {len(rows)} rows\n")

    '''Pubmed - data cleaning: fix or remove inconsistencies'''
    
    log.info(f"Cleaning Pubmed json file")    
    iter = Pubmed.load(rdr.data_iter())
    pubmed_json_rows = list(iter) 
    log.info(f"Pubmed cleaned json output has {len(pubmed_json_rows)} rows\n")

    pubmed_rows = pubmed_csv_rows+ pubmed_json_rows

    '''clinical trials - data loading: reading CSV files'''
    
    log.info(f"Reading clinical trials csv file")
    rdr = CSVPubReader(Path('data\input\clinical_trials.csv'))
    rows = list(rdr.data_iter()) 
    log.info(f"clinical_trials csv file has {len(rows)} rows\n")

    '''clinical trials - data cleaning: fix or remove inconsistencies'''
    
    log.info(f"Cleaning clinical trials json file") 
    iter = ClinicalTrials.load(rdr.data_iter()) 
    clinical_csv_rows = list(iter)
    log.info(f"clinical trials cleaned csv output has {len(clinical_csv_rows)} rows\n")

    
    ''' Data wrangling: Create on the fly json drug graph structure '''

    for i,dic in enumerate(drug_r.data_iter()):
        if i == 0: #Skip header
            continue 
        drug =  dic.get('drug').lower()
    
        for pubmed_dic in pubmed_rows:
            if Publication.is_drug_in_title(drug, pubmed_dic.get('title')):
                Drug.add_pubmed(drug, pubmed_dic.get('title'), pubmed_dic.get('date'))
                Drug.add_journal(drug, pubmed_dic.get('journal'), pubmed_dic.get('date'))
            
        for clinical_dic in clinical_csv_rows:
            if Publication.is_drug_in_title(drug, clinical_dic.get('title')):
                Drug.add_scientific(drug, clinical_dic.get('title'), clinical_dic.get('date'))
                Drug.add_journal(drug, clinical_dic.get('journal'), clinical_dic.get('date'))

    log.debug(f"link graph between drugs and their publications and journals:\n{Drug.get_json()}")
    

    ''' Data wrangling: output drug graph structure in JSON file ''' 
    
    p = Path('./data/output/drug_graph.json')
    with p.open('w+', encoding='utf8') as json_out:
        json_out.write(Drug.get_json())

   
def json_analysis():
    
    ''' Data Analysis: output Journal that mentions the higher number of medicaments '''
    log.info(f"journal with higher number of medicaments is {Drug.get_journal_with_higher_drugs()}")

if __name__ == "__main__":
    
    log_level = logging.INFO
    log_format = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig( stream= sys.stdout, filemode ='w', format=log_format, level=log_level)
    log = logging.getLogger(__name__)

    data_pipeline()
    json_analysis()