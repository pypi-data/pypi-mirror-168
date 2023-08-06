from tunas2dsdl import DetectionParse, Generation
import os
import click


@click.command()
@click.option("-i", "--dataset-info", "dataset_info", type=str, required=True,
              help="The path of the dataset_info.json in tunas format dataset.")
@click.option("-a", "--annotation", "annotation_info", type=str, required=True,
              help="The path of the annotation json file in tunas format dataset.")
@click.option("-w", "--wording-dir", "working_dir", type=str, required=True,
              help="The path of the dataset_info.json in tunas format dataset.")
@click.option("-t", "--task", "task", type=click.Choice(["detection", "classification"]), required=True,
              help="The task type you are working on. 'detection' and 'classification' are available.")
@click.option("-c", "--config", "config", type=str, required=False,
              help="The configuration json file of aliyun oss")
@click.option("-s", "--separate-store", "separate_store_flag", is_flag=True,
              help="Whether to store the samples in json file")
def convert(dataset_info, annotation_info, working_dir, task, config, separate_store_flag):
    assert os.path.isdir(working_dir), f"The working dir '{working_dir}' is not a directory."
    assert len(os.listdir(working_dir)) == 0, f"There have been files in '{working_dir}', which is not permitted."
    if config:
        import json
        with open(config, "r") as f:
            config = json.load(f)

    if task == "detection":
        conversion = DetectionParse(dataset_info, annotation_info, config=config, separate_flag=separate_store_flag)
        generate_obj = Generation(conversion.dsdl_version, conversion.meta_info, conversion.struct_defs,
                                  conversion.class_domain_info, conversion.samples, working_dir,
                                  separate_flag=separate_store_flag)
        class_file = generate_obj.write_class_dom()
        def_file = generate_obj.write_struct_def(file_name="object-detection")
        generate_obj.write_samples(file_name=os.path.basename(annotation_info).replace(".json", ""),
                                   import_list=[class_file, def_file])
    elif task == "classification":
        pass


@click.group()
def cli():
    pass


cli.add_command(convert)

if __name__ == '__main__':
    cli()
