"""Infer the `--limit` for a call to ansible-playbook.

Given an Ansible inventory file (hosts, ini format) and a list of 'changed group/host_vars files'
infer an appropriate `--limit` to be used in a call to `ansible-playbook`.
"""
import configargparse

from ntsbuildtools.ansible import InventoryTree

# __doc__ = __doc__ + InventoryTree.infer_playbook_limit.__doc__


def config_parser(parser: configargparse.ArgParser):
    parser.add_argument(
        'source',
        help='List of all paths of an Ansible Inventory that have been changed.'
    )
    parser.add_argument(
        'inventory',
        help='The path to the relevant (`ini` styled) Ansible hosts file.'
    )

def main(args: configargparse.Namespace):
    # Simplify the playbook limit
    playbook_limit = infer_playbook_limit(args.source, args.inventory)

    # Print the simplified playbook limit to stdout
    print(",".join(list(playbook_limit)))


def infer_playbook_limit(source_path, inventory_path):
    inventory = InventoryTree(inventory_path)
    with open(source_path) as changed_files:
        return inventory.infer_playbook_limit(changed_files.readlines())
