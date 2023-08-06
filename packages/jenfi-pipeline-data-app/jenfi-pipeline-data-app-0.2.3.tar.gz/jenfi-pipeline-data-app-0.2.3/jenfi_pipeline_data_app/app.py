import os
import platform
import tempfile
from pathlib import Path


class Application(object):
    ROOT_DIR = os.path.abspath(os.curdir)
    RESULT_FILENAME = "output.json"
    PYTHON_ENV = os.getenv("PYTHON_ENV", "development")

    from .app_funcs._db_handler import init_db, close_db, db_config
    from .app_funcs._query import df_query, query_one, query_all
    from .app_funcs._parameters import load_test_parameters, get_parameter
    from .app_funcs._result import write_result_to_db, write_result, load_result
    from .app_funcs._models_s3 import push_model_to_s3, load_model_from_s3
    from .app_funcs._test_funcs import (
        __test_direct_module__,
        __test_access_global_var__,
        __test_set_global_var__,
    )

    def boot(self):
        self.init_db()
        self.__init_config_s3()

    def cleanup(self):
        self.close_db()

    def tmp_filepath(self, rel_filepath):
        if self.PYTHON_ENV == "production":
            tmp_path = "/tmp"
        elif self.PYTHON_ENV == "staging":
            tmp_path = "/tmp"
        else:
            tmp_path = Path(
                "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
            )

        return os.path.join(tmp_path, rel_filepath)

    def __init_config_s3(self):
        if self.PYTHON_ENV == "production":
            from .config.s3 import ProductionConfig

            self.s3_config = ProductionConfig()
        elif self.PYTHON_ENV == "staging":
            from .config.s3 import StagingConfig

            self.s3_config = StagingConfig()
        else:
            from .config.s3 import DevelopmentConfig

            self.s3_config = DevelopmentConfig()

        pass

    def __repr__(self):
        return self.__dict__
