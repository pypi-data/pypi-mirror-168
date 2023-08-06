import click
import os

import simplejson

from rastless.config import Cfg
from rastless.core.colormap import create_colormap


@click.command()
@click.argument('sld_file', type=click.Path(exists=True))
@click.option("-n", "--name", help="Name of the colormap, otherwise take the filename")
@click.option("-d", "--description", help="Add description")
@click.option("-l", "--legend-image", help="Filepath to png legend image")
@click.pass_obj
def add_colormap(cfg: Cfg, sld_file, name, description, legend_image):
    """Add a SLD file"""
    if not name:
        name = os.path.basename(sld_file.split(".")[0])
    try:
        color_map = create_colormap(name, sld_file, description, legend_image)
        cfg.db.add_color_map(color_map)
    except Exception as e:
        click.echo(f"SLD File could not be converted. Reason: {e}")


@click.command()
@click.option("-n", "--name", help="Name of the colormap", required=True)
@click.pass_obj
def delete_colormap(cfg: Cfg, name):
    """Remove a SLD file"""
    cfg.db.delete_color_map(name)


@click.command()
@click.pass_obj
def list_colormaps(cfg: Cfg):
    cms = cfg.db.get_color_maps()
    click.echo(simplejson.dumps(cms, indent=4, sort_keys=True))

