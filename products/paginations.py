from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 12  # Number of items per page
    page_query_param = 'page'  # The name of the page parameter URL
    page_size_query_param = 'page_size'  # set the number of items per page via URL
    max_page_size = 20  # The maximum number of items allowed per page


