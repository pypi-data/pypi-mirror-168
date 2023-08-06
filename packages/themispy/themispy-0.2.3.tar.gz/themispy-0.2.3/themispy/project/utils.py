import datetime
import os

import pytz


def split_filepath(url: str) -> 'tuple[str, str]':
    """
    Splits a URL filepath and returns the document name and extension
    as a 2-element tuple.
    
    Args:
        url (str): File URL.
        
    Returns:
        Document name and extension as a 2-element tuple.
        
    """
    docname, docext = os.path.splitext(url)
    docname = docname.rsplit('/')[-1]
    return docname, docext


def format_logpath(tz: str = 'America/Sao_Paulo') -> str:
    """
    Returns the current date properly formatted for logging directories.
    
    Args:
        tz (str): Timezone. (Default is ``America/Sao_Paulo``)
        
    Returns:
        Current date reversed as a string.
        
    Example:
        If today is 14/08/2022 (DD/MM/YYYY), then the function will
    return ``/2022/08/14``.
    
    """
    tz = pytz.timezone(tz)
    return datetime.datetime.now(tz=tz).strftime('/%Y/%m/%d')
