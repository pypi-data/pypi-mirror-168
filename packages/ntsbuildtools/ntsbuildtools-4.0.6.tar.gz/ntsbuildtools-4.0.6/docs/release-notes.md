We attempt to follow semantic versioning for this tool.

> We started tracking Release Notes as of version 3.0.0.

## 4.0.6

* Update "`infer ansible playbook-limit`" CLI endpoint.
    * Ignore any 'vars' section that exist in provided 'inventory (hosts) .ini-style file' 

## 4.0.5

* Refactor "`infer ansible playbook-limit`" CLI endpoint.
  * Rewrite and simplify the 'infer playbook limit' algorithm.
  * Collapse entire `ansible.PlaybookLimit` class to become just the 
    `ansible.InventoryTree.infer_playbook_limit` method.
* Ensure that usage message (e.g. `--help`) is properly filled in.

## 4.0.4

* Refactor internal `ansible.InventoryTree` data structure.
  * Adding unit testing.
  * Simplifying internal building and searching algorithms.

## 4.0.2

* `parse ansible json` CLI endpoint can now parse Ansible *loop* results (recursively).

## 4.0.1

* Fix Python 3.6 support.

## 4.0.0

> Yanked from PyPI due to continued Python 3.6 incompatibility.

* Added support for Python 3.6
* Adding release notes and improve `docs/`. 
* **Backwards incompatible change:** Removed buggy '--tail' argument and code from `post teams card` CLI endpoint.
    * Replaced '--tail' with '--trim'
    * 'trim' cuts off the end of the message instead of the beginning.

## 3.0.2

* Fixed Source Distribution, to include all `docs/` and other required dependencies.
* Rewrite of the CLI framework.
* Rewrite of 'Parsing Ansible JSON' modules/packages, to capture more error messages successfully. 
* Added `--crucial-task` and `--crucial-task-type` filter parameters to `parse ansible json`.
* Addition of `docs/` directory (driven via mkdocs).

## 3.0.1

> Yanked from PyPI due to Broken Source Distribution.

## 3.0.0

> Yanked from PyPI due to Broken Source Distribution.
