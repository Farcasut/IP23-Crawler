class Utils :
    @staticmethod
    def get_rid_of_special_spaces(element):
        return element.replace(u'\xa0', u' ').strip()

