import abc, importlib


class MLComponentBase(metaclass=abc.ABCMeta):
    def __init__(self, modules=None):
        if modules is not None:
            for mo in modules:
                mo_item = importlib.import_module(mo)
                setattr(self, mo, mo_item)

    def __getitem__(self, item):
        return getattr(self, item)

    def load_model(self, model_path):
        pass

    @abc.abstractmethod
    def call(self, linked_item, ori_item=None):
        pass
