import os

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # django < 1.10
    MiddlewareMixin = object


class RangesMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        if response.status_code != 200 or not hasattr(response, 'file_to_stream'):
            return response
        http_range = request.META.get('HTTP_RANGE')
        if not (http_range and http_range.startswith('bytes=') and http_range.count('-') == 1):
            return response
        if_range = request.META.get('HTTP_IF_RANGE')
        if if_range and if_range != response.get('Last-Modified') and if_range != response.get('ETag'):
            return response
        f = response.file_to_stream
        stat_obj = os.fstat(f.fileno())
        start, end = http_range.split('=')[1].split('-')
        if not start:  # requesting the last N bytes
            start = max(0, stat_obj.st_size - int(end))
            end = ''
        start, end = int(start or 0), int(end or stat_obj.st_size - 1)
        assert 0 <= start < stat_obj.st_size, (start, stat_obj.st_size)
        end = min(end, stat_obj.st_size - 1)
        f.seek(start)
        old_read = f.read
        f.read = lambda n: old_read(min(n, end + 1 - f.tell()))
        response.status_code = 206
        response['Content-Length'] = end + 1 - start
        response['Content-Range'] = 'bytes %d-%d/%d' % (start, end, stat_obj.st_size)
        return response
