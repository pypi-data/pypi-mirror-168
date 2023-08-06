from abc import abstractmethod


class BaseDataClass:
    def to_dict(self):
        return self.__dict__


class BaseConfiguration:
    config: BaseDataClass

    def dumps(self):
        return self.config.to_dict()


class AbstractDataLoader:
    @abstractmethod
    def dumps(self):
        pass

    @abstractmethod
    def from_config(self):
        pass
