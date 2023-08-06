from typing import Union, List

from hbutils.string import plural_word

from ...model import MappingBasedModel, MemoryStatus, GenericCollection


class GPUCollection(GenericCollection):
    def __getitem__(self, item) -> Union[List['GPU'], 'GPU']:
        return GenericCollection.__getitem__(self, item)

    def __str__(self):
        return GenericCollection.__str__(self)

    def __repr__(self):
        return f'<{type(self).__name__} {plural_word(len(self), "gpu")}>'


class NvidiaMemoryStatus(MemoryStatus):
    def __init__(self, data):
        MemoryStatus.__init__(self, data['total'], data['used'], data['free'])


class FBMemoryUsage(NvidiaMemoryStatus):
    pass


class GPU(MappingBasedModel):
    def __init__(self, data):
        MappingBasedModel.__init__(self, data)

    @property
    def id(self) -> str:
        return self['@id']

    @property
    def name(self) -> str:
        return self['product_name']

    @property
    def brand(self) -> str:
        return self['product_brand']

    @property
    def memory(self) -> FBMemoryUsage:
        return FBMemoryUsage(self["fb_memory_usage"])

    @property
    def _better_name(self):
        if not self.brand or self.brand in self.name:
            return self.name
        else:
            return f'{self.brand} {self.name}'

    def _str_format(self):
        return f'<{type(self).__name__} {self._better_name}, {self.uuid}, {self.memory.total}>'

    def __str__(self):
        return self._str_format()

    def __repr__(self):
        return self._str_format()
