import random
from utils import Utils

u = Utils()
gi = u.gi

history_name = 'bioblend-workflow-' + str(random.randrange(1000000))

history, datamap = u.setup_history(history_name, [
    {'id': 'c2e192f7-6f43-4454-b4c7-d0b4fddc7018', 'file': 'data/ligands_x1.sdf', 'file_type': 'sdf'},
    {'id': '0a31acf6-f534-4402-a672-9ca6d3c60176', 'file': 'data/refmol.mol', 'file_type': 'mol'},
    {'id': 'ebb6b00d-15cd-4c2d-b63a-7f569bac0573', 'file': 'data/receptor.pdbqt', 'file_type': 'pdbqt'},
])

workflow_id = 'f2db41e1fa331b3e'
workflow = gi.workflows.show_workflow(workflow_id)

u.run_workflow(workflow, history, datamap, './tmp')

print('Results are in the directory tmp')