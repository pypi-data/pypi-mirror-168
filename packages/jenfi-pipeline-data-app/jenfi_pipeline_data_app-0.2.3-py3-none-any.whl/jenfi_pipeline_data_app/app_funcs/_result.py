import json
import numpy as np
import pandas as pd

from decimal import Decimal
from datetime import date, datetime


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return super(NpEncoder, self).default(obj)

    def _preprocess_nan(self, obj):
        if isinstance(obj, float) and np.isnan(obj):
            return None
        elif isinstance(obj, dict):
            return {
                self._preprocess_nan(k): self._preprocess_nan(v) for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [self._preprocess_nan(i) for i in obj]
        return obj

    def iterencode(self, obj):
        return super(NpEncoder, self).iterencode(self._preprocess_nan(obj))


def write_result_to_db(self, logical_step_name, state_machine_run_id):
    from ..db_models import StateMachineRun

    return StateMachineRun().result_to_db(
        logical_step_name, state_machine_run_id, self.load_result()
    )


def write_result(self, result):
    with open(self.tmp_filepath(self.RESULT_FILENAME), "w") as f:
        json.dump(result, f, cls=NpEncoder)

    return self.tmp_filepath(self.RESULT_FILENAME)


def load_result(self):
    with open(self.tmp_filepath(self.RESULT_FILENAME), "r") as result:
        output_data = json.load(result)

        return output_data
