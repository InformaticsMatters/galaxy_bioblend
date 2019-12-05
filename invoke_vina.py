from galaxyclient import Workflow
import time, random

#workflow_id = 'f2db41e1fa331b3e'
workflow_id = 'bd92053d47e530b7'

history_name = 'bioblend-vina-' + str(random.randrange(1000000))

# these must be in the right order as required by the workflow as the 'inputs_by'
# parameter of invoke_workflow does not seem to work in this version
inputs = [
    {'file': 'data/vina/refmol.mol', 'file_type': 'mol'},
    {'file': 'data/vina/receptor.pdbqt', 'file_type': 'pdbqt'},
    {'file': 'data/vina/ligands_x1.sdf', 'file_type': 'sdf'}
]

# step 3 is prepare_box
# step 4 is docking
# params have step id as key and dict of param names/values
paramsmap = {
    '3': {'bufx': 1.0, 'bufy': 1.0, 'bufz': 1.0},
    '4': {'exh': 5, 'ph_value': 6.4}
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

