import threading
from datetime import datetime


class ThreadLocal(object):
    """ThreadLocal is a object that is responsible to store some attributes on thread local storage."""

    _storage = threading.local()

    @staticmethod
    def set_rabbitmq_task_start_time(time: int = None):
        """
        This method is responsible to set RabbitMQ execution start time attribute on Thread storage.
        :param time: the actual time
        :type time: int
        """
        start_time = time or datetime.now()
        ThreadLocal._put("start_time", start_time)

    @staticmethod
    def get_rabbitmq_task_start_time():
        """
        This method is responsible to get RabbitMQ execution start time attribute on Thread storage.
        """
        start_time = ThreadLocal._get("start_time")
        if not start_time:
            return None
        else:
            delta = datetime.now() - start_time
            return delta.total_seconds()

    @staticmethod
    def set_request_id(uuid: str):
        """
        This method is responsible to set request_id attribute for each Task execution.
        :param uuid: the hash of request id
        :type uuid: str
        """
        ThreadLocal._put("request_id", str(uuid))

    @staticmethod
    def get_request_id():
        """
        This method is responsible to get request_id attribute for each Task execution.
        """
        return ThreadLocal._get("request_id")

    @staticmethod
    def clear():
        """
        This method clean attributes that were persisted on Thread local storage.
        """
        ThreadLocal._storage.__dict__.clear()

    @staticmethod
    def _put(key, value):
        """
        This method adds an attribute on Thread local storage.
        """
        setattr(ThreadLocal._storage, key, value)

    @staticmethod
    def _get(key):
        """
        This method gets an attribute on Thread local storage.
        """
        if hasattr(ThreadLocal._storage, key):
            return getattr(ThreadLocal._storage, key)
        else:
            return None
