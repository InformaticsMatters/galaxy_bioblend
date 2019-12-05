from galaxyclient import Utils
import sys

u = Utils()
gi = u.get_galaxy_instance()

ids = []
if len(sys.argv) == 1:
    workflows = gi.workflows.get_workflows()
    for w in workflows:
        ids.append(w['id'])
else:
    ids = sys.argv[1:]

for id in ids:
    workflow = gi.workflows.show_workflow(id)
    print("Workflow: " + str(workflow))