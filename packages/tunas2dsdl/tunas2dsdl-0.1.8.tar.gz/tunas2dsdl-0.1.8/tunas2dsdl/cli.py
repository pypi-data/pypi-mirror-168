from tunas2dsdl import DetectionParse, Generation
import os
import click
from tunas2dsdl import OptionEatAll
from tunas2dsdl.general import prepare_input


@click.command(name='convert')
@click.option("-d", "--directory", "directory", type=str,
              help="The directory path of the whole tunas v0.3 dataset.")
@click.option("-i", "--dataset-info", "dataset_info", type=str,
              help="The path of the dataset_info.json in tunas format dataset.")
@click.option("-a", "--annotation", "annotation_info", cls=OptionEatAll, type=str,
              help="The path of the annotation json file in tunas format dataset.")
@click.option("-w", "--wording-dir", "working_dir", type=str, required=True,
              help="The working directory where you want to generate the dsdl yaml files.")
@click.option("-t", "--task", "task", type=click.Choice(["detection", "classification"]), required=True,
              help="The task type you are working on. 'detection' and 'classification' are available.")
@click.option("-c", "--config", "config", type=str, required=False,
              help="The configuration json file of aliyun oss")
@click.option("-s", "--separate-store", "separate_store_flag", is_flag=True,
              help="Whether to store the samples in json file")
@prepare_input
def convert(directory, dataset_info, annotation_info, working_dir, task, config, separate_store_flag):
    if task == "detection":
        for seg_name, ann_file in annotation_info.items():
            conversion = DetectionParse(dataset_info, ann_file, separate_flag=separate_store_flag, file_client=config)
            this_work_dir = os.path.join(working_dir, seg_name)
            assert not os.path.isdir(this_work_dir), f"'{this_work_dir}' have existed, which is not permitted."
            os.mkdir(this_work_dir)
            generate_obj = Generation(conversion.dsdl_version, conversion.meta_info, conversion.struct_defs,
                                      conversion.class_domain_info, conversion.samples, this_work_dir,
                                      separate_flag=separate_store_flag)
            class_file = generate_obj.write_class_dom()
            def_file = generate_obj.write_struct_def(file_name=f"{seg_name}_object-detection")
            generate_obj.write_samples(file_name=seg_name, import_list=[class_file, def_file])
    elif task == "classification":
        pass


@click.group()
def cli():
    pass


cli.add_command(convert)

if __name__ == '__main__':
    cli()
