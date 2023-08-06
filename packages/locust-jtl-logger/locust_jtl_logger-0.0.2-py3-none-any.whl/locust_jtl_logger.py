import csv


class LocustJTLLogger:
    def __init__(self, locust_env, filename='jtl.csv', buffer=8096):
        self.locust_env = locust_env
        self.filename = filename
        self.buffer = buffer
        env = self.locust_env.events
        env.test_start.add_listener(self._start)
        env.test_stop.add_listener(self._stop)
        env.request.add_listener(self._log_request)

    def _headers(self):
        return [
            'timeStamp', 'elapsed', 'label', 'responseCode', 'responseMessage', 'threadName', 'dataType', 'success',
            'failureMessage', 'bytes', 'sentBytes', 'grpThreads', 'allThreads', 'URL', 'Latency', 'IdleTime', 'Connect'
        ]

    def _start(self, environment, **kw):
        self.fh = open(self.filename, 'w', newline='', buffering=self.buffer)
        self.csv = csv.writer(self.fh)
        self.csv.writerow(self._headers())
        self.fh.flush()

    def _stop(self, environment, **kw):
        self.fh.flush()
        self.fh.close()

    def _log_request(self, request_type, name, response_time, response_length,
                     response, context, exception, start_time, url, **kwargs):
        label_name = context.get('name_param', name)
        self.csv.writerow([
            round(start_time * 1000),
            round(response_time),
            f'{request_type} {label_name}',
            response.status_code,
            response.reason,
            'locust',
            'text',
            response.ok,
            str(exception) if exception else '',
            response_length,
            context.get('bytes_sent', '0'),
            '0',
            '0',
            url,
            round(response_time - (response.elapsed.microseconds/1000)),
            '0',
            '0'
        ])
