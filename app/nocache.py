class NoCache(object):
    def process_response(self, request, response):
        """
        set the "Cache-Control" header to "must-revalidate, no-cache"
        """
        if request.path.startswith('/static/') or request.path.startswith('/templates/'):
            response['Cache-Control'] = 'must-revalidate, no-cache'
        return response