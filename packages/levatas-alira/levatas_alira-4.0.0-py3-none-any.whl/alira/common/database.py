import logging
import os
import sqlalchemy as db

from alira.instance import Instance
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base


DeclarativeBase = declarative_base()

FIRST_INSTANCE_COLUMNS = [  # The 'instances' table columns to be included in flat instances
    "creation_date",
    "mission_id",
    "waypoint_id",
    "prediction"
]


class Instances(DeclarativeBase):
    __tablename__ = "instances"

    instance_id = db.Column(db.VARCHAR(36), primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pipeline_id = db.Column(db.VARCHAR(32), nullable=False)

    prediction = db.Column(db.Integer, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    files = db.Column(db.JSON(), nullable=True)
    waypoint_id = db.Column(db.VARCHAR(64), nullable=True)
    mission_id = db.Column(db.VARCHAR(64), nullable=True)
    source_id = db.Column(db.VARCHAR(32), nullable=True)
    instance_metadata = db.Column(db.JSON(), nullable=True)
    instance_properties = db.Column(db.JSON(), nullable=True)


class Database:
    def __init__(self, url: str = None, test_engine = None):  # test_engine parameter is just for unit tests
        self.url = url or "mysql+pymysql://root:{}@alira-mysql:{}/alira".format(
            os.environ.get("MYSQL_ROOT_PASSWORD"),
            os.environ.get("MYSQL_PORT")
        )
        self.test_engine = test_engine

    def instance_dao(self):
        return InstanceDAO(self.url, test_engine=self.test_engine)

    def flat_instance_metadata_dao(self, pipeline_id: str):
        return FlatInstanceMetadataDAO(self.url, pipeline_id, test_engine=self.test_engine)


class BaseDAO:
    def __init__(self, url: str, test_engine=None):
        if test_engine is None:
            self.engine = db.create_engine(url)
        else:
            self.engine = test_engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class InstanceDAO(BaseDAO):
    def __init__(self, url: str, test_engine=None):
        super(InstanceDAO, self).__init__(url, test_engine)

    def get_instance(self, instance_id: str):
        return self.session.query(Instances).filter(Instances.instance_id == instance_id).first()

    def get_pipeline_instances(self, pipeline_id: str = None, limit: int = 100):
        limit = max(min(limit, 500), 1)

        query = self.session.query(Instances).order_by(Instances.creation_date.desc())
        if pipeline_id:
            query = query.filter(Instances.pipeline_id == pipeline_id)

        return query.limit(limit).all()

    def put(self, instance: Instance):
        instance_from_table = self.get_instance(instance_id=instance.instance_id)

        if instance_from_table:
            instance_from_table.creation_date = instance.creation_date
            instance_from_table.last_update_date = instance.last_update_date
            instance_from_table.pipeline_id = instance.pipeline_id
            instance_from_table.prediction = instance.prediction
            instance_from_table.confidence = instance.confidence
            instance_from_table.files = instance.files
            instance_from_table.waypoint_id = instance.waypoint_id
            instance_from_table.mission_id = instance.mission_id
            instance_from_table.source_id = instance.source_id
            instance_from_table.instance_metadata = instance.instance_metadata
            instance_from_table.instance_properties = instance.instance_properties

            self.session.commit()
        else:
            instance_row = Instances(
                instance_id=instance.instance_id,
                creation_date=instance.creation_date,
                last_update_date=instance.last_update_date,
                pipeline_id=instance.pipeline_id,
                prediction=instance.prediction,
                confidence=instance.confidence,
                files=instance.files,
                waypoint_id=instance.waypoint_id,
                mission_id=instance.mission_id,
                source_id=instance.source_id,
                instance_metadata=instance.instance_metadata,
                instance_properties=instance.instance_properties
            )

            self.session.add(instance_row)
            self.session.commit()

        return instance


class FlatInstanceMetadataDAO(BaseDAO):
    def __init__(self, url: str, pipeline_id: str, test_engine=None):
        super(FlatInstanceMetadataDAO, self).__init__(url, test_engine)
        AutoMapBase = automap_base()
        AutoMapBase.prepare(autoload_with=self.engine)
        metadata = db.MetaData(bind=self.engine)

        metadata.reflect()
        self.table = None
        self.Model = None
        if pipeline_id in metadata.tables:
            self.table = metadata.tables[pipeline_id]
            self.Model = getattr(AutoMapBase.classes, pipeline_id)
        self.pipeline_id = pipeline_id

    def get_flat_instance_metadata(self, instance_id: str):
        return self.session.query(self.table).filter(self.table.columns.instance_id == instance_id).first()

    def get_flat_instances(self):
        # We split the instance columns into two groups for CSV order (FIRST_INSTANCE_COLUMNS and last_instance_columns)
        last_instance_columns = [column.name for column in Instances.__table__.columns if
                                 (column.name not in FIRST_INSTANCE_COLUMNS)
                                 and (column.name not in ["instance_id", "pipeline_id"])
                                 and (str(column.type) != "JSON")
                                 ]

        flat_instance_metadata_columns = []
        query = self.session.query(Instances).filter(Instances.pipeline_id == self.pipeline_id)

        # If the pipeline-specific instance table exists, enrich column list and query with its data
        if self.table is not None:
            flat_instance_metadata_columns = self.table.columns.keys()
            query = query.join(self.table, Instances.instance_id == self.table.columns.instance_id)

        columns = FIRST_INSTANCE_COLUMNS + flat_instance_metadata_columns + last_instance_columns

        results = query.order_by(Instances.creation_date.desc()).with_entities(
            *(list(getattr(Instances, column) for column in FIRST_INSTANCE_COLUMNS)
              + list(getattr(self.table.columns, column) for column in flat_instance_metadata_columns)
              + list(getattr(Instances, column) for column in last_instance_columns)
              )
        ).all()

        return columns, results

    def put(self, instance: Instance):
        if self.table is None:
            logging.info(f"There does not seem to be a MySQL table for pipeline '{self.pipeline_id}'")
            return

        instance_metadata: dict = instance.instance_metadata

        kwargs = dict()
        for col in self.table.columns:
            if col.name == "instance_id":
                kwargs["instance_id"] = instance.instance_id
            elif col.name in instance_metadata:
                kwargs[col.name] = instance_metadata[col.name]
        self.session.add(self.Model(**kwargs))
        self.session.commit()
