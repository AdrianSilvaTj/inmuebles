from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class PropertyPagination(PageNumberPagination):
    page_size = 5
    page_query_params = 'p'
    page_size_query_params = 'size'
    max_page_size = 10
    last_page_strings = 'end'
    
class PropertyLimitOffsetPag(LimitOffsetPagination):
    """ Offset: Cantidad de registros desde donde va a comenzar la pagination
    Limit: cantidad de registros """
    default_limit = 1