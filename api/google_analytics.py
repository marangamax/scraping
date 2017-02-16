import google_oauth2 as oauth2
import sys
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from httplib import BadStatusLine


class API_call:
    
    def __init__(self, ga_ids, query_name):
        self.ga_ids = ga_ids
        self.query_name = query_name
        try:
            self.google_query = Retriever(self.ga_ids, self.query_name)
        except:
            print "False ga_ids or query name"
            sys.exit(1)
        self.query_results = [lines for page in iter(self.google_query) for lines in page['rows']]
        self.api_entries_num = page['totalResults']
        self.api_headers = page['query']['dimensions'].encode('utf-8').split(",")+ [metric.encode('utf-8') for metric in page['query']['metrics']]
    
class Retriever:

    MAX_RESULTS = '100000'

    def __init__(self, ids, enquiry):
    
        self.__service = oauth2.authenticate('analytics', 'v3', 'https://www.googleapis.com/auth/analytics.readonly')

        self.__ids = ids
        self.__enquiry = enquiry
        self.profiles_index = 0
        self.page_index = 1
        self.last_page = None

    def __iter__(self):
        return self
        
    def return_ids(self):
        return self.__ids

    def next(self):
        try:
            return self.fetch()
        except StopIteration:
            self.profiles_index += 1
            if not self.profiles_index < len(self.__ids):
                raise StopIteration
            self.page_index = 1
            self.last_page = None
            return self.next()

    def fetch(self):
        if self.last_page is not None and \
                not self.last_page.get('nextLink'):
            raise StopIteration
        try:
            results = self.__fetch()
            self.page_index += int(self.MAX_RESULTS)
            self.last_page = results
            return results

        except TypeError, error:
            # Handle errors in constructing a query.
            print ('There was an error in constructing your query : %s' % error)
            raise error

        except HttpError:
            # we move on, if possible, to the next venture
            raise StopIteration

        except AccessTokenRefreshError:
            # Handle Auth errors.
            print ('The credentials have been revoked or expired, please re-run the application to re-authorize')

    def __fetch(self):
        """
        we give it 3 chances, than I just fail
        parameters must be passed as lists
        """
        error = None # hopefully
        for attempt in [1, 2, 3]:
            try:
                return self.__service.data().ga().get(
                    ids='ga:%s' % self.__ids[self.profiles_index],
                    start_date=self.__enquiry.start_date,
                    end_date=self.__enquiry.end_date,
                    metrics=','.join(self.__enquiry.metrics) if len(self.__enquiry.metrics) > 0 else None,
                    segment=''.join(self.__enquiry.segment) if len(self.__enquiry.segment) > 0 else None,
                    dimensions=','.join(self.__enquiry.dimensions) if len(self.__enquiry.dimensions) > 0 else None,
                    sort=None,
                    filters=','.join(self.__enquiry.filters) if len(self.__enquiry.filters) > 0 else None,
                    start_index=str(self.page_index),
                    max_results=self.MAX_RESULTS).execute()

            except HttpError, error:
                # Handle API errors.
                print >> sys.stderr, ("[%s/3] gAPI's %s : %s" % (attempt, error.resp.status, error._get_reason()))

            except BadStatusLine, error:
                print >> sys.stderr, ("[%s/3] HTTP BadStatusLine" % attempt)

        raise error


class Enquiry:

    def __init__(self, start_date, end_date, metrics, segment=[], dimensions=[], filters=[]):
        self.start_date = start_date
        self.end_date = end_date
        self.metrics = metrics
        self.segment = segment
        self.dimensions = dimensions
        self.filters = filters

if __name__ == "__main__":
    import doctest
    doctest.testmod()
