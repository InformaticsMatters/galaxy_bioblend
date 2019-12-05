from galaxyclient import Workflow
import random, time

# workflow_id = '' # docker
workflow_id = 'd6af45a5b4f240e0' # eu

history_name = 'bioblend-rdock-score-filter-' + str(random.randrange(1000000))

# these must be in the right order as required by the workflow as the 'inputs_by'
# parameter of invoke_workflow does not seem to work in version 0.13
# The order that is needed is the key (integer) of the inputs dict, NOT the
# order in which they appear
inputs = [

    {'file': 'data/nudt7/receptor.mol2', 'file_type': 'mol2'},
    {'file': 'data/nudt7/receptor.as', 'file_type': 'rdock_as'},
    {'file': 'data/nudt7/follow_up_candidates.sdf', 'file_type': 'sdf'},
    {'file': 'data/nudt7/ligand.mol', 'file_type': 'mol'},
]

# step 4 is splitter
# step 5 is rdock
# step 6 is sucos
# params have step id as key and dict of param names/values
paramsmap = {
    '5': {'num': 5},
}


##### work starts from here

start = time.time()

w = Workflow(history_name, workflow_id)
inputsmap = w.upload_inputs(inputs)
w.invoke_workflow(inputsmap, paramsmap)
w.wait_for_workflow_to_complete()
count = w.download_outputs('./tmp')


print(str(count) + ' results are in the directory tmp')

finish = time.time()
print("Done in " + str(finish - start) + 'secs')



