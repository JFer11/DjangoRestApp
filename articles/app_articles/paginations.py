from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class MyPaginationArticles(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 6

    def get_asc_or_desc(self, request):
        return request.headers.get('Sort', None)

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []

        order = self.get_asc_or_desc(request)
        if order == 'DESC':
            queryset = queryset.order_by('-created')
        elif order == 'ASC':
            queryset = queryset.order_by('created')
        elif order is None:
            # No order requested
            pass

        return list(queryset[self.offset:self.offset + self.limit])


class MyPaginationUsers(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 12
