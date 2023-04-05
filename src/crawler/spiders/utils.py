
# gets rid of &nbsp;
def get_rid_of_special_spaces(element):
    if element is not None:
        return element.replace(u'\xa0', u' ').strip()
    else:
        return None
