from galaxyclient import Utils

u = Utils()
gi = u.get_galaxy_instance()

workflows = gi.workflows.get_workflows()
for workflow in workflows:
     print("Workflow: " + str(workflow))