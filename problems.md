# Problems encountered

## Workflow completion

As Galaxy gives you a `invocation` object when you start a workflow and that object has a `state`
property you might expect to be able to find out when the workflow is completed by fetching the
invocation object at a regular interval. But the final state that is reported is `scheduled` 
so you can only tell that your workflow has been scheduled, not that it completed.

Instead what you need to do is look at all the steps of the workflow, get the job IDs from those
that have them and then to query those jobs for their status. Those report `ok` when that are
finished.

This fairly painful logic can be found in the `get_job_ids()`, `are_jobs_ok()` and `wait_on_jobs()`
methods in the Utils class (see utils.py).

**Suggested improvement**: provide better information on the invocation state allowing to find out
if it is complete, and if so whether it completed successfully or not.

**Update**: problem subsequently encountered with the job IDs being missing from some of the steps
resulting in it being impossible to determine if the workflow is complete. This may be a new problem
in 19.09 (can't be certain about this but it seemed to work OK in 19.01)

## Determining outputs

You might think that the `invocation` object would give you a handle on the outputs created by the
workflow, and indeed there are `outputs` and `output_collections` properties. Unfortunately these
don't work as expected:

1. they have contents when the workflow is first invoked, but have disappeared by the time
execution is complete
2. the values that `outputs` and `output_collections` contain are wrong! In one case where
one output and one output_collection is expected I get 2 outputs and 0 output_collection, and
one of the outputs is from a completely different history!

According to [this converstion](https://gitter.im/galaxyproject/bioblend?at=5d97581f5173c33ca169282f)
this is likely a bug in Galaxy.

**Suggested improvement**: provide the correct information in the `outputs` and `output_collections`
properties and ensure this information does not disappear.

**Update**: the problem with the **wrong** datasets looks to be a misunderstanding of how to use the
Galaxy API (the ID of the dataset is identified by the `id` property not the `dataset_id` property!)
but the fundamental problem of the missing `outputs` and `output_collections` remains.

## Uploading files.

I am unable to upload `mol2` format files as imputs in 19.09. This appears to be because the mol2 format
id defined as being not `visible`. This worked OK in 19.01 and the `visible` setting has not changed.
Simon from Freiburg cannot reproduce this which is strange. The `visible` seeting for `mol2` datatype is 
being changed whihc will work around the problem.

## Workflow steps not being scheduled

In the case of a workflow step having an input parmeter (as oposed to a dataset) being defined by a 
previous step the step does no appear to be scheduled if preveious steps fail due to errors and then
get manually re-executed. Only when all steps execute successfully first time does that type of step
get scheduled.

## Slow execution of trivial steps

A workflow can have trivial steps taking only a few ms to execute, but depending on the state of the 
galaxy environment those steps can take minutes to schedule and execute.
