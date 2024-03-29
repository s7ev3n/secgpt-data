"""Base class for SEC filings."""
from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

class FilingType(str, Enum):
    TenK = "10-K"
    TenQ = "10-Q"
    EightK = "8-K"

# For filing info, refer to https://sec-api.io/docs/query-api
class FilingInfo:
    accession_no: str  # accession number of filing. Example: 0000065011-21-000020
    cik: str           # CIK of filer. Trailing zeros are removed. Example: 65011
    company_name: str  # (string) : company name of the filer. Example: MEREDITH CORP (MDP) (CIK 0000065011)
    ticker: str        # (string) : if available, ticker of the filer. Example: AAPL for Apple Inc.
    description: str   # (string) : description of the document. Example: EXHIBIT 99 FY21 Q2 EARNINGS PRESS RELEASE
    form_type: str     # (string) : filing type. Example: 8-K
    filing_url: str    # (string) : URL of the filing or attachement. Example: https://www.sec.gov/Archives/edgar/data/65011/000006501121000020/fy21q2exh99earnings.htm
    filing_date: str   # (string) : date of filing. Format: yyyy-mm-dd Example: 2021-02-04}


class BaseFiling:
    """ A thin wrapper of SEC filing data. """
    
    """
    data :
    A dict containing all the processed text from one filing report,
    with each section name as the key, and value is the text.
    See constants.py for keys for different types of filing, 
    e.g. FILING_10_K_SECTIONS
    """
    data : Optional[Dict[str, Any]] = None
    filing_info : FilingInfo = None

    """
    extra_info :
    - as part of meta info to LLMs as context
    - as filtering info for vector database
    """
    extra_info : Optional[Dict[str, Any]] = None

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        """ Get filing type """
    
    def set_filing_info(self, info : FilingInfo) -> None:
        """ set filing info """
        self.filing_info = info
    
    def from_dict(self, data : Dict[str, Any]) -> None:
        """ set filing data """
        self.data = data

    def get_data_by_section(self, section_key : str) -> str:
        """Get filing section text given supported section item keys"""

        assert self.data is not None, \
            'No filing data, use from_dict() to fill the data first'
        assert section_key in self.data.keys(), \
            'Not supported section item'
        
        return self.data[section_key]
    
    def get_data(self) -> dict:
        """Get the data dict"""
        assert self.data is not None, \
            'No filing data, use from_dict() to fill the data first'
        
        return self.data

    def get_filing_info(self) -> FilingInfo:
        """ Get filing info """
        assert self.filing_info is not None, \
            "Not set filing info, please set_filing_info() first"
        
        return self.filing_info
    