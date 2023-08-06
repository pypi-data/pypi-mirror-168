import itertools
import logging
import os
from configparser import ConfigParser, NoSectionError
from dataclasses import dataclass, field
from functools import reduce
from typing import List, Set

logger = logging.getLogger(__name__)


def flatten(lst):
    return [item for sublist in lst for item in sublist]


@dataclass
class InventoryNode:
    """Represents a host or group of hosts.

    Has a name and parent/children relationships.
    """
    name: str
    children: Set['InventoryNode'] = field(default_factory=set)
    parents: Set['InventoryNode'] = field(default_factory=set)

    def __hash__(self):
        return hash(self.name)

    def add_child(self, child):
        """Add a child to this nodes children."""
        self.children.add(child)

    def add_parent(self, parent):
        """Add a parent to this nodes parents."""
        self.parents.add(parent)

    def get_ancestors(self) -> Set['InventoryNode']:
        """Return the set of ancestors of this node.
        """
        if self.parents:
            ancestors = reduce(Set.union, map(InventoryNode.get_ancestors, self.parents))
            return self.parents.union(ancestors)
        else:
            return set()

    def get_younglings(self):
        if self.children:
            younglings = reduce(Set.union, map(InventoryNode.get_younglings, self.children))
            return self.children.union(younglings)
        else:
            return set()

    def __str__(self):
        return self.name

    def __repr__(self):
        """Creates a useful representation for debugging.

        Returns:
            str: This object with parents and children listed as strings.
        """
        children_names = [child.name for child in self.children]
        parent_names = [parent.name for parent in self.parents]
        return f'InventoryNode(name={self.name}, children=set({children_names}), parents=set({parent_names}))'


def strip_ansible_group_name_metadata(group_name):
    return group_name.replace(':children', '') 


class InventoryTree:
    def __init__(self, path: str):
        """Ansible Inventory.

        Enables traversing and querying an Ansible Inventory (e.g. your ini-style "hosts" file).

        Args:
            path (str): Path to the Ansible Inventory config file, your ini-style `hosts` file.
        """
        self.nodes = set()
        self.root = set()
        self._config = ConfigParser(allow_no_value=True)
        self._config.read(path)
        self._init_nodes()
        self._init_nodes_relationships()
        self._init_root()

    def groups_from_config(self):
        section_names = self._config.sections()
        return list(filter(lambda name: not name.endswith(':vars'), section_names))

    def group_members_from_config(self, group_name):
        try:
            return self._config.options(group_name)
        except NoSectionError:
            return self._config.options(f'{group_name}:children')

    def get_node(self, name: str) -> InventoryNode:
        """Find node in this tree.

        Does not ensure the node name is unique -- will return first node with name. 
        """
        name = strip_ansible_group_name_metadata(name)
        for node in self.nodes:
            if node.name == name:
                return node
        raise LookupError(f'Unable to find Ansible Inventory item with name: {name}')

    def infer_playbook_limit(self, files_touched: List[str], minimize=True) -> List[str]:
        """Infer an Ansible 'Playbook Limit' from a list of 'touched [host|group]_vars files.'

        This can be very useful for Continuous Integration (CI) of Ansible playbooks.

        Args:
            files_touched (List[str]): List of Ansible inventory files changed (only care 
                changes to host_vars and group_vars). 
            minimize (bool, optional): Remove any groups that are redundant. Defaults to True.

        Example:
            Imagine using Git to track an Ansible project. Your goal is to determine the 
            `--limit` argument for a call to `ansible-playbook` in your CI pipeline. 

            If using GitHub Flow for the project, you can a list of files_touched 
            like the following:

            ```
            git diff origin/main --name-only --ignore-all-space \
                | grep -E "group_vars|host_vars" > files_touched.txt
            ```

            This method can take the files_touched.txt as input like the following, 

                >>> inventory = InventoryTree('tests/testresources/ansible-hosts-example')
                >>> with open('tests/testresources/files_touched.txt') as files_touched:
                ...     inventory.infer_playbook_limit(files_touched.readlines())
                ['dc-leafs', 'dr-gws']

            The produced list can be used as the `--limit` argument for a call to `ansible-playbook`.

        Returns:
            List[str]: Simplified list of groups/hosts from this Ansible Inventory, to be used as playbook_limit.
        """
        limits = []
        for file_path in files_touched:
            split_file_path = file_path.split(os.path.sep)
            if split_file_path[-2] == 'group_vars' or split_file_path[-2] == 'host_vars':
                limits.append(split_file_path[-1].strip())
            else:
                logger.warning(f'Encountered non-inventory file: {file_path}')
        return self.simplify_playbook_limit(limits, minimize)

    def simplify_playbook_limit(self, hosts_groups_touched: List[str], minimize=True) -> List[str]:
        """Simplify an Ansible 'Playbook Limit' based on a list of 'touched hosts/groups'
        """
        nodes = set([ self.get_node(name) for name in hosts_groups_touched ])

        removals = set()
        additions = set()
        first_run = True
        while removals or additions or first_run:
            first_run = False

            # 0. Process changes, removals take precedence
            nodes = nodes.union(additions)
            additions.clear()
            nodes -= removals
            removals.clear()

            #
            # 1. Remove any hosts/groups if they are already represented by another limit
            #   If the playbook limit includes one of my ancestors, then I am already included in the limits via that group!
            #
            for node in nodes:
                if node.get_ancestors().intersection(nodes):
                    removals.add(node)

            #
            # 2. Check if the playbook limit includes ALL the children of some group
            #   Add the group and remove ALL the children
            #
            parents = set().union(*[ node.parents for node in nodes ])
            parents = parents.difference(nodes)
            for parent in parents: 
                if parent.children.issubset(nodes):
                    removals = removals.union(parent.children)
                    additions.add(parent)

            #
            # 3. Finally, Check if any groups are redundant
            #
            if minimize and not removals and not additions:
                for nodeA, nodeB in itertools.combinations(nodes, 2):
                    if nodeA.children and nodeA.children.issubset(nodeB.get_younglings()):
                        removals.add(nodeA)

        return sorted([limit.name for limit in nodes])

    def _init_nodes(self):
        """Add all hosts and groups to the tree."""
        for group_name in self.groups_from_config():
            self.nodes.add(InventoryNode(strip_ansible_group_name_metadata(group_name)))
            for host_or_group_name in self.group_members_from_config(group_name):
                self.nodes.add(InventoryNode(host_or_group_name))

    def _init_nodes_relationships(self):
        """Establish parent-child relationships within this tree.

        Expects all the nodes to already be initialized.
        """
        groups = [self.get_node(group_name) for group_name in self.groups_from_config()]
        for group in groups:
            group_members = self.group_members_from_config(group.name)
            for host_or_group_name in group_members:
                host_or_group = self.get_node(host_or_group_name)
                group.add_child(host_or_group)
                host_or_group.add_parent(group)

    def _init_root(self):
        """Establish the root set of this tree.

        TODO: Discuss what this really means.

        Expects parent-child relationships to already be established within this tree.
        """
        for node in self.nodes:
            if not node.parents:
                self.root.add(node)
