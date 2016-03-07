'''
    Helper Functions
'''

def _parse_affiliation(affilixml):
    institution = affilixml.find('affilname').text
    city = affilixml.find('affiliation-city').text
    country = affilixml.find('affiliation-country').text
    return institution + ', ' + city + ', ' + country

def _parse_author(authorxml):
    author_id = authorxml.find('dc:identifier').text.split(':')[-1]
    lastname = authorxml.find('surname').text
    firstname = authorxml.find('given-name').text
    document_count = int(authorxml.find('document-count').text)
    # affiliations
    affil = authorxml.find('affiliation-current')
    institution = affil.find('affiliation-name').text
    #city = affil.find('affiliation-city').text
    #country = affil.find('affiliation-country').text
    #affiliation = institution + ', ' + city + ', ' + country

    return {'author_id': author_id, 'name': firstname + ' ' + lastname, 'document_count': document_count,\
            'affiliation': institution}
    
def _parse_xml(xml):
    # {{{ _parse_xml
    try:
        scopus_id = xml.find('dc:identifier').text.split(':')[-1]
    except:
        scopus_id = None
    try:
        title = xml.find('dc:title').text
    except:
        title = None
    try:
        publicationname = xml.find('prism:publicationname').text
    except:
        publicationname = None
    try:
        issn = xml.find('prism:issn').text
    except:
        issn = None
    try:
        isbn = xml.find('prism:isbn').text
    except:
        isbn = None
    try:
        eissn = xml.find('prism:eissn').text
    except:
        eissn = None
    try:
        volume = xml.find('prism:volume').text
    except:
        volume = None
    try:
        pagerange = xml.find('prism:pagerange').text
    except:
        pagerange = None
    try:
        coverdate = xml.find('prism:coverdate').text
    except:
        coverdate = None
    try:
        doi = xml.find('prism:doi').text
    except:
        doi = None
    try:
        citationcount = int(xml.find('citedby-count').text)
    except:
        citationcount = None
    try:
        affiliation = _parse_affiliation(xml.find('affiliation'))
    except:
        affiliation = None
    try:
        aggregationtype = xml.find('prism:aggregationtype').text
    except:
        aggregationtype = None
    try:
        sub_dc = xml.find('subtypedescription').text
    except:
        sub_dc = None

    return {'scopus_id': scopus_id, 'title': title, 'publication_name':publicationname, 'issn': issn, 'isbn': isbn, \
            'eissn': eissn, 'volume': volume, 'page_range': pagerange, 'cover_date': coverdate, 'doi': doi, \
            'citation_count': citationcount, 'affiliation': affiliation, 'aggregation_type': aggregationtype, \
            'subtype_description': sub_dc}
    #}}}

def trunc(s,min_pos=0,max_pos=75,ellipsis=True):
    #{{{

    """Truncation beautifier function
    This simple function attempts to intelligently truncate a given string
    """
    __author__ = 'Kelvin Wong <www.kelvinwong.ca>'
    __date__ = '2007-06-22'
    __version__ = '0.10'
    __license__ = 'Python http://www.python.org/psf/license/'

    """Return a nicely shortened string if over a set upper limit 
    (default 75 characters)
    
    What is nicely shortened? Consider this line from Orwell's 1984...
    0---------1---------2---------3---------4---------5---------6---------7---->
    When we are omnipotent we shall have no more need of science. There will be
    
    If the limit is set to 70, a hard truncation would result in...
    When we are omnipotent we shall have no more need of science. There wi...
    
    Truncating to the nearest space might be better...
    When we are omnipotent we shall have no more need of science. There...
    
    The best truncation would be...
    When we are omnipotent we shall have no more need of science...
    
    Therefore, the returned string will be, in priority...
    
    1. If the string is less than the limit, just return the whole string
    2. If the string has a period, return the string from zero to the first
        period from the right
    3. If the string has no period, return the string from zero to the first
        space
    4. If there is no space or period in the range return a hard truncation
    
    In all cases, the string returned will have ellipsis appended unless
    otherwise specified.
    
    Parameters:
        s = string to be truncated as a String
        min_pos = minimum character index to return as Integer (returned
                  string will be at least this long - default 0)
        max_pos = maximum character index to return as Integer (returned
                  string will be at most this long - default 75)
        ellipsis = returned string will have an ellipsis appended to it
                   before it is returned if this is set as Boolean 
                   (default is True)
    Returns:
        Truncated String
    Throws:
        ValueError exception if min_pos > max_pos, indicating improper 
        configuration
    Usage:
    short_string = trunc(some_long_string)
    or
    shorter_string = trunc(some_long_string,max_pos=15,ellipsis=False)
    """
    # Sentinel value -1 returned by String function rfind
    NOT_FOUND = -1
    # Error message for max smaller than min positional error
    ERR_MAXMIN = 'Minimum position cannot be greater than maximum position'
    
    # If the minimum position value is greater than max, throw an exception
    if max_pos < min_pos:
        raise ValueError(ERR_MAXMIN)
    # Change the ellipsis characters here if you want a true ellipsis
    if ellipsis:
        suffix = '...'
    else:
        suffix = ''
    # Case 1: Return string if it is shorter (or equal to) than the limit
    length = len(s)
    if length <= max_pos:
        return s + suffix
    else:
        # Case 2: Return it to nearest period if possible
        try:
            end = s.rindex('.',min_pos,max_pos)
        except ValueError:
            # Case 3: Return string to nearest space
            end = s.rfind(' ',min_pos,max_pos)
            if end == NOT_FOUND:
                end = max_pos
        return s[0:end] + suffix
    # }}}