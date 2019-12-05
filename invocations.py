from galaxyclient import Utils

u = Utils()
gi = u.get_galaxy_instance()

invocations = gi.invocations.get_invocations()

print(str(invocations))

