from aiopsconnector.base import Configuration
from requests import request


class ConnectorService:
    def __init__(self):
        pass

    @classmethod
    def create_model_train(cls, user: str, data: dict):
        """To deliver data to ai-api-service.
        it goes to postgresql Consequently.
        For model-train-management.
        :param user(str): Jupyter Notebook User(=Kubeflow user)
        :param data(dict): Dictionary data object.
        :return:
        """
        try:
            conf = Configuration()
            target_uri = conf.sc + '/management/model_train/'
            data['user_email'] = user
            response = request(url=target_uri, method='post', json=data)
            return response
        except Exception as e:
            return e

    @classmethod
    def create_model_applied_detection(cls, user: str, data: dict):
        """To deliver data to ai-api-service.
        It goes to postgresql consequently.
        For model-applied-detection-management.
        :param user(str): Jupyter Notebook User(=Kubeflow user)
        :param data: Dictionary data object.
        :return:
        """
        try:
            conf = Configuration()
            target_uri = conf.sc + '/management/model_applied_detection/'
            data['user_email'] = user
            response = request(url=target_uri, method='post', json=data)
            return response
        except Exception as e:
            return e
