import click
from . import scoring
from . import utils

import pandas as pd
import logging

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.0.1')
def sprawl():
    """
    cli for SRRS to detect subcellular RNA localization patterns
    """
    pass


@sprawl.command()
@click.argument('filename', type=click.Path(exists=True))
def validate(filename):
    """
    Validate that [filename] hdf5 is in a usable format for SRRS
    """
    #TODO just echoing back the file name, need to implement the actual logic
    click.echo(click.format_filename(filename))


@sprawl.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option('--metric', type=click.Choice(scoring.available_metrics.keys()), required = True)
def gene_cell_scoring(**kwargs):
    """
    Calculate gene/cell scores of an HDF5 [input] file using one of the spatial metrics and save as a CSV to the [output] file
    """
    #TODO not sure if I want to bother adding this functionality to the cli
    input_str = click.format_filename(kwargs['input'])
    output_str = click.format_filename(kwargs['output'])
    click.echo('Will score {} using {} and output to {}'.format(input_str, kwargs['metric'], output_str))


@sprawl.command()
@click.argument('bam', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.argument('mapping', type=click.Path())
@click.option('--processes', type=int, required=False)
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")
def annotate(**kwargs):
    """
    Annotate a bam file with a custom tag using cell-type or other mapping
    
    Arguments:
        * bam is the path to the sorted/index bam file 
        * output is the path where the annotated bam will be created 
        * mapping is a two-column CSV where the headers are the "from"-tag and the "dest"-tag 
    """
    mapping_df = pd.read_csv(kwargs['mapping'])
    key_tag,val_tag = mapping_df.columns
    mapping = dict(mapping_df.values)
    logging_level=logging.DEBUG if kwargs['verbose'] else logging.INFO

    utils.map_bam_tag(
        kwargs['bam'],
        kwargs['output'],
        mapping, 
        key_tag=key_tag, 
        val_tag=val_tag, 
        processes=kwargs.get('processes',1),
        logging_level=logging_level,
    )


if __name__ == '__main__':
    sprawl()

