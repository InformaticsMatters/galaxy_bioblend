from utils import Utils

u = Utils()

workflows = u.get_workflows()
for workflow in workflows:
     print("Workflow: " + str(workflow))