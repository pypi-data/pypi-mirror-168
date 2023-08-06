from sqlalchemy.engine import Engine
from pathlib import Path
import pandas as pd

from .cacher import Cacher


class DbCache(object):
    def __init__(
        self,
        db_engine: Engine,
        logical_step_name: str,
        state_machine_run_id: str,
        local_cache_dir: Path,
        s3_bucket_name: str,
    ) -> None:
        self.db_engine = db_engine
        self.cacher = Cacher(
            logical_step_name, state_machine_run_id, local_cache_dir, s3_bucket_name
        )

        pass

    def df_query(self, query_str: str, rebuild_cache: bool) -> pd.DataFrame:
        return self._with_cacher(self._df_query, query_str, rebuild_cache)

    def _df_query(self, query_str: str) -> pd.DataFrame:
        return pd.read_sql(query_str, self.db_engine)

    def _with_cacher(self, query_func, query_str: str, rebuild_cache: bool):
        if self.cacher.exists(query_str) and not rebuild_cache:
            return self.cacher.from_cache(query_str)
        else:
            result = query_func(query_str)

            self.cacher.to_cache(query_str, result)

            return result
