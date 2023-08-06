from sqlalchemy import Table, MetaData, Column, JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from .__init__ import PipelineDataApp as app

from sqlalchemy.orm.attributes import flag_modified

Base = declarative_base()
metadata = MetaData(bind=app.db_engine)


class StateMachineRun(Base):
    __table__ = Table(
        "pipeline_state_machine_runs",
        metadata,
        Column("result", MutableDict.as_mutable(JSON)),
        autoload=True,
    )

    def result_to_db(self, logical_step_name, state_machine_run_id, results):
        sm_run = app.db.query(StateMachineRun).get(state_machine_run_id)
        sm_run.result[logical_step_name] = results

        return app.db.commit()
