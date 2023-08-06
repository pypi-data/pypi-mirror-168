import boto3
import pickle


def push_model_to_s3(self, model, model_key):
    pickle_byte_obj = pickle.dumps(model)

    __s3_model_obj(self, model_key).put(Body=pickle_byte_obj)

    pass


def load_model_from_s3(self, model_key):
    # Model => S3 => Download Model
    obj = __s3_model_obj(self, model_key)

    return pickle.loads(obj.get()['Body'].read())


def __s3_model_obj(self, model_key):
    bucket_name = self.s3_config.S3_TRAINED_MODELS_BUCKET
    fileprefix = self.get_parameter("logical_step_name")  # Supposed to be step_name
    filename = f"{fileprefix}_{model_key}.pickle"

    s3 = boto3.resource("s3")

    return s3.Object(bucket_name, filename)
