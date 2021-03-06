import requests, json, os, time, traceback
from pydantic import BaseSettings

curr_datetime = time.time_ns()

# initialize the loki client class
class Loki:
    def __init__(self, url=None, config=None, **tags):
        if url:
            self.url = url
        if isinstance(config, BaseSettings):
            self.url = config.url
        else:
            try:
                self.url = os.environ["LOKI_URL"]
            except KeyError:
                print("Please set the LOKI_URL environment variable")
                exit(1)
        # create a dict from the kwargs
        self.tags = tags

    # function to post logs to loki
    def info(self, msg, **tags):
        # Constructing the payload
        curr_datetime = time.time_ns()
        # append the class tags to the tags
        tags.update(self.tags)
        payload = json.dumps(
            {"streams": [{"stream": tags, "values": [[curr_datetime, f"[INFO] {msg}"]]}]}
        )
        # Posting the payload
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url, data=payload, headers=headers)
        if r.status_code != 204:
            print("Error posting to Loki")
        else:
            print(f"[INFO] {msg}")

    def warning(self, msg, **tags):
        # Constructing the payload
        curr_datetime = time.time_ns()
        # append the class tags to the tags
        tags.update(self.tags)
        payload = json.dumps(
            {"streams": [{"stream": tags, "values": [[curr_datetime, f"[WARNING] {msg}"]]}]}
        )
        # Posting the payload
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url, data=payload, headers=headers)
        if r.status_code != 204:
            print("Error posting to Loki")
        else:
            print(f"[WARNING] {msg}")

    def error(self, msg, exception=None, **tags):
        # Constructing the payload
        curr_datetime = time.time_ns()
        # append the class tags to the tags
        tags.update(self.tags)
        if not exception:
            payload = json.dumps(
                {
                    "streams": [
                        {
                            "stream": tags,
                            "values": [
                                [curr_datetime, f"[ERROR] {msg} \n {traceback.format_exc()}"]
                            ],
                        }
                    ]
                }
            )
        else:
            payload = json.dumps(
                {
                    "streams": [
                        {
                            "stream": tags,
                            "values": [
                                [
                                    curr_datetime,
                                    f"[ERROR] {msg} \n {''.join(traceback.format_exception(etype=type(exception),value=exception,tb=exception.__traceback__))}",
                                ]
                            ],
                        }
                    ]
                }
            )
        # Posting the payload
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url, data=payload, headers=headers)
        if r.status_code != 204:
            print("Error posting to Loki")
        else:
            print(f"[ERROR] {msg}")
            # print(traceback.format_exc())
