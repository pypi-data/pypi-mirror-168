import sys
import os
import platform
import tempfile
from pathlib import Path


class Application(object):
    ROOT_DIR = os.path.abspath(os.curdir)
    RESULT_FILENAME = "output.json"
    PYTHON_ENV = os.getenv("PYTHON_ENV", "development")

    from .app_funcs._db_handler import _init_db, _close_db, _db_config
    from .app_funcs._query import df_query, query_one, query_all, _db_cache
    from .app_funcs._parameters import load_test_parameters, get_parameter, _run_data
    from .app_funcs._result import (
        write_result_to_db,
        write_result,
        load_result,
        _remove_result_file,
    )
    from .app_funcs._models_s3 import (
        push_model_to_s3,
        load_model_from_s3,
        _init_config_s3,
    )

    def boot(self):
        self._init_db()
        self._init_config_s3()

    def cleanup(self):
        self._close_db()
        self._remove_result_file()

    def tmp_dir(self) -> Path:
        if self.PYTHON_ENV == "production":
            tmp_path = "/tmp"
        elif self.PYTHON_ENV == "staging":
            tmp_path = "/tmp"
        else:
            tmp_path = (
                "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
            )

        return Path(tmp_path)

    def tmp_filepath(self, rel_filepath) -> Path:
        tmp_path = self.tmp_dir()

        return Path(os.path.join(tmp_path, rel_filepath))

    def __repr__(self):
        return self.__dict__

    if "pytest" in sys.modules:
        from .app_funcs._test_funcs import (
            _test_direct_module,
            _test_access_global_var,
            _test_set_global_var,
        )
