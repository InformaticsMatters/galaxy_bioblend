# Examples of running Galaxy workflows using Bioblend

This repo provides examples of how to execute Galaxy workflows using Python and 
 Bioblend.

* Galaxy docs: https://docs.galaxyproject.org/en/master/index.html
* Bioblend user docs: https://bioblend.readthedocs.io/en/latest/index.html
* Bioblend API docs: https://bioblend.readthedocs.io/en/latest/api_docs/galaxy/all.html#

## Setup

Copy `galaxy-config-template.yml` to `galaxy-config.yml` and then edit the new file
with you Galaxy server URL and API key.

## General procedure

1. Create your workflow in Galaxy using the Galaxy UI, making sure you define the necessary
inputs and outputs and give these meaningful but simple names.
2. Test the workflow in Galaxy to ensure that it runs, using some suitable test data.
3. Provide access to test inputs (e.g. in the data directory).
4. Write a workflow executor wrapper, typically named as exec_xyz.py.
5. Execute the wrapper.
 
Use an existing executor to get an idea of what to do. You need to define the workflow ID
and provide the necessary information about the inputs.

## Execution logic

The execution of a workflow proceeds as follows:

1. A new empty Galaxy history is created to work in.
2. The inputs are uploaded into that history.
3. The workflow with the specified ID is started with the given inputs. 
4. Wait for the workflow to complete.
5. Download and new datasets that were created by workflow execution.

Note: currently the history is **NOT** deleted so you need to do that in the Galaxy UI. 

## TODO

The current implementations are very basic and probably only support limited types of
workflows. Improvements expected include:

* Handle workflow parameters.
* History cleanup
* Error handling when workflow fails
* Allow inputs to be specifeed as command line arguments 

## Problems

A number of problems and issues were encountered in creating these tools. These are summarised
[here](problems.md).

## Tools

### 1. list_workflows.py

This tool lists the available workflows in Galaxy.

```bash
 python list_workflows.py
```

### 2. show_workflows.py

This tool shows details of the workflows listed by the list_workflows.py tool.

```bash
 python list_workflows.py
```
 
### 3. exec_vina.py

This tool executes a workflow that performs docking using Autodock VINA, including
generating the box parameters using a pre-defined ligand.

You need that workflow to be present in Galaxy (TODO - provide the workflow once all the 
tools are present on usegalaxy.eu).

```bash
 python exec_vina.py
```


