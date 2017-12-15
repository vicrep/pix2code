__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

from keras.models import model_from_json
from tensorflow.python.lib.io.file_io import FileIO
import os

class AModel:
    def __init__(self, input_shape, output_size, output_path):
        self.model = None
        self.input_shape = input_shape
        self.output_size = output_size
        self.output_path = output_path
        self.name = ""

    def save(self):
        model_json = self.model.to_json()
        with FileIO("{}/{}.json".format(self.output_path, self.name), "w") as json_file:
            json_file.write(model_json)

        fp = "{}.h5".format(self.name)

        if self.output_path.startswith('gs://'):
            self.model.save_weights(fp)
            copy_file_to_gcs(self.output_path, fp)
        else:
            self.model.save_weights("{}/{}.h5".format(self.output_path, self.name))

    def load(self, name=""):
        output_name = self.name if name == "" else name
        with FileIO("{}/{}.json".format(self.output_path, output_name), "r") as json_file:
            loaded_model_json = json_file.read()
        self.model = model_from_json(loaded_model_json)

        fp = "{}.h5".format(output_name)

        if self.output_path.startswith('gs://'):
            copy_file_from_gcs(self.output_path, fp)
            self.model.load_weights(fp)
        else:
            self.model.load_weights("{}/{}.h5".format(self.output_path, output_name))

def copy_file_to_gcs(job_dir, file_path):
  with FileIO(file_path, mode='r') as input_f:
    with FileIO(os.path.join(job_dir, file_path), mode='w+') as output_f:
        output_f.write(input_f.read())

def copy_file_from_gcs(job_dir, file_path, outfilepath=None):
    to_path = outfilepath if outfilepath is not None else file_path
    with FileIO(os.path.join(job_dir, file_path), mode='r') as input_f:
        with FileIO(to_path, mode='w+') as output_f:
            output_f.write(input_f.read())
