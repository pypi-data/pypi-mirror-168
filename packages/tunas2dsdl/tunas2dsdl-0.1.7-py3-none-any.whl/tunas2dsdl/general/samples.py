from .utils import Util


class DataSample:
    def __init__(self, struct, class_domain):
        self.sample_struct = struct
        self.class_domain = class_domain
        self.samples = []

    def add_item(self, item, pre_format=True):
        if pre_format:
            sample = self.add_quotes(item.copy())
            for k, v in sample.items():
                if Util.is_list_of(v, dict):
                    sample[k] = [Util.fmap(_) for _ in v]
            self.samples.append(sample)
        else:
            self.samples.append(item)

    def add_quotes(self, sample):
        if isinstance(sample, dict):
            for k, v in sample.items():
                sample[k] = self.add_quotes(v)
        elif isinstance(sample, list):
            for k, v in enumerate(sample):
                sample[k] = self.add_quotes(v)
        elif isinstance(sample, str):
            sample = Util.add_quotes(sample)

        return sample

    @property
    def sample_type(self):
        return f"{self.sample_struct.name}[{self.sample_struct.ARG}={self.class_domain.name}]"

    def format(self, file_name="local"):
        content = dict()
        content["sample-type"] = self.sample_type
        content["sample-path"] = file_name
        content["samples"] = self.samples
        return {"data": content}
