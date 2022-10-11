from motor import motor_asyncio

from config import config


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(
            config.MONGO_DATABASE_URI_WITH_AUTH,
            connect=True,
            maxPoolSize=200,
        )

        self._db = self._client[config.MONGO_DATABASE_NAME]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo_instance = Mongo()
mongo_client = mongo_instance.client
mongo_db = mongo_instance.db
