import sqlalchemy as db

from alira.common.database import Database
from alira.instance import Instance
from alira.modules.module import Connection
from sqlalchemy.orm import sessionmaker

PIPELINE_REMOTE_DATABASE_MODULE_NAME = "remotedatabase"


# TODO Since we are planning to retire support for Rest servers, this module has not been tested at all, and thus may not work properly
class RemoteDatabase(Connection):
    def __init__(
            self,
            url: str,
            configuration_directory: str,
            **kwargs
    ):
        super().__init__(
            configuration_directory=configuration_directory,
            module_id=PIPELINE_REMOTE_DATABASE_MODULE_NAME,
            **kwargs,
        )
        self.url = url
        engine = db.create_engine(url)
        Session = sessionmaker(bind=engine)
        self.remote_session = Session()

    def run(self, instance: Instance, **kwargs):
        super().run(instance, **kwargs)
        database = Database(self.url)
        database.instance_dao().put(instance)
        database.flat_instance_metadata_dao(instance.pipeline_id).put(instance)
