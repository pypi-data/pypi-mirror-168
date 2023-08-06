import requests
from .items import Item


class Queue(object):
    """
    Class to manage queues in the robot manager console.
    With this class you can create, update and get queues from Orchestrator.
    Arguments:
        connection: Connection object to connect to the robot manager console.
        queue_name: Name of the queue.
        queue_id    : ID of the queue.
        robot_id : ID of the robot.
    Attributes:
        connection: Connection object to connect to the robot manager console.
        queue_name: Name of the queue.
        queue_id    : ID of the queue.
        robot_id : ID of the robot.
    Methods:
        create_item(item_data): Create a new item in the queue.
        get_next_item(): Get the next pending item in the queue.
        set_retry_times(times): Set the retry times of an item.
    """

    def __init__(self, **kwargs):

        self.connection = kwargs.get('connection')
        self.queue_id = kwargs.get('queue_id', None)
        self.queue_name = kwargs.get('queue_name', None)
        self.robot_id = kwargs.get('robot_id', None)
        self.__get_queue()
        self.__retry_times = 1

    def __get_queue(self):
        """
        Get Queue from Orchestrator
        Returns:
            Queue: queue object.
        """
        if self.queue_id is None:
            end_point = f'{self.connection.http_protocol}{self.connection.url}/api/robots/{self.robot_id}/add_queue/'
            data = {
                'QueueName': self.queue_name
                }
            response = requests.post(end_point, data, headers=self.connection.headers)
            self.queue_id = response.json()['QueueId']
        else:
            end_point = f'{self.connection.http_protocol}{self.connection.url}/api/queues/?QueueId={self.queue_id}'
            response = requests.get(end_point, headers=self.connection.headers)
            if response.status_code != 200:
                raise Exception(response.json())
            self.queue_name = response.json()[0]['QueueName']

    def __getItem(self):
        """
        Get all items from Queue
        Return:
            Item: Yields pending items from Queue.
        """
        endpoint = f'{self.connection.http_protocol}{self.connection.url}/api/items/?QueueId={self.queue_id}&Status=pending'
        try:
            response = requests.get(endpoint, headers=self.connection.headers)
            if response.status_code != 200:
                raise Exception(response.json())
            queue_items = response.json()
        except Exception as exception_message:
            raise Exception(exception_message)
        for item in queue_items:
            item = Item(connection=self.connection, queue_id=self.queue_id, item_id=item['ItemId'],item_data=item['Data'])
            if item.status == 'fail' and item.item_executions < self.__retry_times:
                item.set_item_executions()
                item.set_item_as_pending()
            if item.status == 'pending':
                item.set_item_as_working()
                yield item

    def create_item(self, item_data: dict):
        """
        Create New Item in The Orchestrator
        Arguments:
            item_data: Dictionary with the item data.
        """
        item = Item(connection=self.connection, queue_id=self.queue_id, item_data=item_data)
        return item

    def get_next_item(self):
        """
        Get Next Pending item from Orchestrator
        Returns:
            Item: The next item from the queue.
        """
        try:
            item = next(self.__getItem())
        except:
            item = None
        return item

    def set_retry_times(self, times: int):
        """
        Set number of retry times for each item
        Arguments:
            times: Number of retry times.
        """
        self.__retry_times = times
