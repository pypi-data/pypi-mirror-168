import abc


class TrainableProcessModelBase(metaclass=abc.ABCMeta):

    def __init__(self, name: str):
        self._name = name

    @property
    def Name(self):
        return self._name

    def __call__(self, *args, **kwargs):
        self.call(args[0], )

    @abc.abstractmethod
    def call(self, input, train_mode=False):
        pass

    @abc.abstractmethod
    def update_parameters(self, act_result, exp_result):
        pass

    @abc.abstractmethod
    def load(self, model_key: str):
        pass

    @abc.abstractmethod
    def save(self, model_key: str):
        pass
