from galaxyclient import Workflow
import random, time

history_name = 'bioblend-rdock-sucos-' + str(random.randrange(1000000))

# workflow_id = 'a799d38679e985db' # docker
workflow_id = '7422d72fffb95e9a' # eu

inputs = [
    {'file': 'data/nudt7/receptor.mol2', 'file_type': 'mol2'},
    {'file': 'data/nudt7/receptor.as', 'file_type': 'rdock_as'},
    {'file': 'data/nudt7/follow_up_candidates.sdf', 'file_type': 'sdf'},
    {'file': 'data/nudt7/ligand.mol', 'file_type': 'mol'},
]

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

