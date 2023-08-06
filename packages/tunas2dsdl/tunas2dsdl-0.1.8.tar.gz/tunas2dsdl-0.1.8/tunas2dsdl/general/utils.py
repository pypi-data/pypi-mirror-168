import click

try:
    import ruamel_yaml as yaml
    from ruamel_yaml import YAML
except ImportError:
    import ruamel.yaml as yaml
    from ruamel.yaml import YAML
from ..io import FileIO, PetrelBackend, AliyunOSSBackend, HardDiskBackend
import os


class Util:

    @staticmethod
    def is_list_of(obj, cls):
        if isinstance(obj, list):
            return isinstance(obj[0], cls)
        return False

    @staticmethod
    def add_quotes(string):
        # string = f'"{string}"'
        string = yaml.scalarstring.DoubleQuotedScalarString(string)
        return string

    @staticmethod
    def flist(x):
        x = [Util.add_quotes(_) for _ in x]
        retval = yaml.comments.CommentedSeq(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval

    @staticmethod
    def fmap(x):
        retval = yaml.comments.CommentedMap(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval


class OptionEatAll(click.Option):
    """
    implemented by https://stackoverflow.com/users/7311767/stephen-rauch in https://stackoverflow.com/questions/48391777/nargs-equivalent-for-options-in-click
    """

    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(OptionEatAll, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


def prepare_input(func):
    def process(directory, dataset_info, annotation_info, working_dir, task, config, separate_store_flag):

        assert os.path.isdir(working_dir), f"The working dir '{working_dir}' is not a directory."

        if config:
            import json
            with open(config, "r") as f:
                config = json.load(f)

        if directory is not None:
            assert not (
                    dataset_info or annotation_info), "You have specified the directory, which means you don't need to specify the paths of annotation file and `dataset_info.json`."
            if FileIO.is_ceph_path(directory):
                file_client = PetrelBackend()
                dataset_info = os.path.join(directory, 'dataset_info.json')
                ann_dir = os.path.join(directory, 'annotations', 'json',)
                annotation_info = [os.path.join(ann_dir, _) for _ in file_client.listdir(ann_dir) if _.endswith('.json')]
            elif FileIO.is_oss_path(directory):
                assert config, "you must provide the configuration of aliyun oss."
                bucket_name = FileIO.get_bucket_name(directory)
                file_client = AliyunOSSBackend(bucket_name=bucket_name, **config)
                dataset_info = os.path.join(directory, 'dataset_info.json')
                dataset_info = FileIO.get_oss_rel_path(dataset_info)
                if directory.endswith("/"):
                    directory = directory[:-1]
                ann_dir = '/'.join([directory, 'annotations', 'json'])
                annotation_info = [_ for _ in file_client.listdir(ann_dir) if _.endswith('.json')]
            else:
                file_client = HardDiskBackend()
                dataset_info = os.path.join(directory, 'dataset_info.json')
                ann_dir = os.path.join(directory, 'annotations', 'json')
                annotation_info = [os.path.join(ann_dir, _) for _ in file_client.listdir(ann_dir) if
                                   _.endswith('.json')]

        else:
            assert dataset_info and annotation_info, "The directory of dataset is not speicified, which means you need to specify the paths of annotation file and `dataset_info.json` with '-a' and '-i'"
            if FileIO.is_ceph_path(dataset_info):
                file_client = PetrelBackend()
                annotation_info = [_ for _ in annotation_info if _.endswith('.json')]
            elif FileIO.is_oss_path(dataset_info):
                assert config, "you must provide the configuration of aliyun oss."
                bucket_name = FileIO.get_bucket_name(dataset_info)
                bucket_name_ = FileIO.get_bucket_name(annotation_info)
                assert bucket_name_ == bucket_name, "the files must be from the same bucket."
                file_client = AliyunOSSBackend(bucket_name=bucket_name, **config)
                dataset_info = FileIO.get_oss_rel_path(dataset_info)
                annotation_info = [FileIO.get_oss_rel_path(_) for _ in annotation_info if _.endswith('.json')]
            else:
                file_client = HardDiskBackend()
                annotation_info = [_ for _ in annotation_info if _.endswith('.json')]

        annotation_info = {os.path.basename(_).split('.')[0]: _ for _ in annotation_info}
        return directory, dataset_info, annotation_info, working_dir, task, file_client, separate_store_flag

    def wrapper(*args, **kwargs):
        ret = process(*args, **kwargs)
        ret = func(*ret)
        return ret

    return wrapper

def get_segment_name(filepath):
    segment = os.path.basename(filepath).split('.')[0]
    return segment
