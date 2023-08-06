import datetime
import os
import string
import warnings
from pathlib import Path
from random import random
import requests
from decouple import config


class OrchestratorAPI:
    """
    Class that handles the communication with the orchestrator.

    """

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        self.token = kwargs.get('token', None)
        self.parameters = kwargs.get('params', None)
        self.debug = False
        self.debug_data = None
        self.___connection = self.__check_connection()
        self.http_protocol = self.__get_protocol()
        self.ws_protocol = self.__get_ws_protocol()
        self.url = self.__get_url()
        self.headers = {'Authorization': f'Token {self.token}'}

    def __check_connection(self):
        """
        This method is used to check if the connection with the orchestrator is working.
        Returns:
             True if the connection is working, False otherwise.
        """
        if self.token is None:
            self.debug = True
            if config('IBOTT_URL', default=None) is None:
                folder = Path(os.path.dirname(os.path.realpath(__file__))).parent
                env_file = os.path.join(folder, '.env')
                with open(env_file, 'a') as f:
                    IBOTT_URL = str(input("Write iBott Console url: "))
                    f.write(f"IBOTT_URL = \"{IBOTT_URL}\"")
                f.close()
                self.url = IBOTT_URL
            else:
                self.url = config('IBOTT_URL', default=None)
            if config('IBOTT_TOKEN', default=None) is None:
                folder = Path(os.path.dirname(os.path.realpath(__file__))).parent
                env_file = os.path.join(folder, '.env')
                with open(env_file, 'a') as f:
                    IBOTT_TOKEN = str(input("Write iBott Console token: "))
                    f.write("\n")
                    f.write(f"IBOTT_TOKEN = \"{IBOTT_TOKEN}\"")
                f.close()
                self.token = IBOTT_TOKEN
            else:
                self.token = config('IBOTT_TOKEN', default=None)
            warnings.warn(
                f"Using enviroment variables to connect to the orchestrator")
        return True

    def __get_protocol(self):
        """
        This method is used to get the protocol of the iBott API.
        Returns:
            http_protocol: str
        """
        if "https://" in self.url:
            return "https://"
        return "http://"

    def __get_ws_protocol(self):
        """
        This method is used to get the websocket protocol of the iBott API.
        Returns:
             websocket protocol
        """
        if "https://" in self.url:
            return "wss://"
        return "ws://"

    def __get_url(self):
        """
        This method is used to get the url of the iBott API.
        Returns:
            url: str
        """
        if "https://" in self.url:
            self.url = self.url.replace("https://", "")
        else:
            self.url = self.url.replace("http://", "")
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        return self.url

    def send_message(self, message, log_type='log'):
        """
        Async method used to send a message to the orchestrator.
        Arguments:
            message: str
            log_type: str
        Returns:
            response: dict
        """
        """
        send log to robot manage console
        Arguments:
            message {string} -- message to send
            log_type {string} -- type of the log
        """

        endpoint = f'{self.http_protocol}{self.url}/api/logs/'
        log_data = {
            "LogType": log_type,
            "LogData": message,
            "ExecutionId": self.execution_id,
            "LogId": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64)),
            "DateTime": datetime.datetime.now()
        }
        try:
            requests.post(endpoint, log_data, headers=self.headers)
        except Exception as e:
            print(e)

    @classmethod
    def get_args(cls, args):
        """
        Get arguments from command line
        Arguments:
            args: list
        Returns:
            args: dict
            """
        if len(args) > 1:
            args = eval(args[1].replace("'", '"'))
        else:
            args = {
                'RobotId': None,
                'ExecutionId': None,
                'url': None,
                'token': None,
                'params': None
            }
        return args
