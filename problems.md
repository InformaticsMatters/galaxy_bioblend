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
