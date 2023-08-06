import click
import simplejson

from rastless.config import Cfg
from rastless.db.models import PermissionModel


@click.command()
@click.option('-p', '--permission', required=True, type=str,
              help='Role e.g role#<client>:<client_role>, user#<username>')
@click.option('-l', '--layer_ids', help='Layer id', required=True, type=str, multiple=True)
@click.pass_obj
def add_permission(cfg: Cfg, permission, layer_ids):
    """Add a role to one or multiple layers."""
    permissions = [PermissionModel(permission=permission, layer_id=layer) for layer in layer_ids]
    cfg.db.add_permissions(permissions)
    click.echo("Role was successfully added to layers")


@click.command()
@click.option('-p', '--permissions', help='Permission name e.g role#<client>:<client_role>, user#<username>',
              required=True, type=str, multiple=True)
@click.pass_obj
def delete_permission(cfg: Cfg, permissions):
    """Delete one or multiple permissions."""

    for permission in permissions:
        cfg.db.delete_permission(permission)

    click.echo("Roles were successfully deleted")


@click.command()
@click.option("-p", "--permission", help='Permission name e.g role#<client>:<client_role>, user#<username>',
              required=True, type=str)
@click.option('-l', '--layer_id', help='Layer id', type=str)
@click.pass_obj
def delete_layer_permission(cfg: Cfg, permission, layer_id):
    """Delete layer permission."""

    cfg.db.delete_layer_from_layer_permission(layer_id, permission)

    click.echo("Layer permission was successfully deleted")


@click.command()
@click.option('-l', '--layer_id', help='Layer id', type=str)
@click.option('-p', '--permission', type=str,
              help='Role e.g role#<client>:<client_role>, user#<username>')
@click.pass_obj
def get_permissions(cfg: Cfg, layer_id, permission):
    items = []

    if permission:
        items = cfg.db.get_layers_for_permission(permission)

    if layer_id:
        items = cfg.db.get_permission_for_layer_id(layer_id)

    click.echo(simplejson.dumps(items, indent=4, sort_keys=True))
