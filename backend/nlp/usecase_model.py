from . import uml_model


class Model(uml_model.Model):
    def __init__(self):
        self.train_path_name = 'usecase'
        self.data_path_name = 'usecase_data'
        self.startModel()
