from django.views.debug import ExceptionReporter
import requests

from sentinel_django import Authentication


class SentinelExceptionReporter(ExceptionReporter):
    def get_traceback_data(self):
        data = super(SentinelExceptionReporter, self).get_traceback_data()
        self.send_to_sever(data)
        return data

    def send_to_sever(self, data):
        frame = data['frames'][0]
        rep = {
            "name": data.get('exception_type'),
            "filename": frame.get('filename'),
            "desc": data.get('exception_value'),
            "function_name": frame.get('function'),
            "line_number": frame.get('lineno'),
            "route": data.get('request_insecure_uri'),
            "request": str(data.get('request')),
            "meta": str(data.get('request').headers),
            "project": Authentication().token
        }
        # "https://asFocHSDEONCaPdHlwTPlqlpXhUMpuIQaSFOnMRVonWSRytYqQvfjpTKYAdi.ziton.live"
        stack_trace = list()
        for frame in data['frames']:
            retrace = {
                'filename': frame.get('filename'),
                'function': frame.get('function'),
                'lineno': frame.get('lineno'),
                'pre_context': frame.get('pre_context'),
                'context_line': "➡" + frame.get('context_line'),
                'post_context': frame.get('post_context'),
                'pre_context_lineno': frame.get('pre_context_lineno'),
            }
            stack_trace.append(retrace)
        rep["django_error"] = stack_trace
        r = requests.post("https://api.ziton.live/api/django/", json=rep)
