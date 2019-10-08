from utils import Utils

u = Utils()
workflows = u.get_workflows()
for w in workflows:
    workflow = u.show_workflow(w['id'])
    print("Workflow: " + str(workflow))