from galaxyclient import Utils
import sys

args = sys.argv

u = Utils()
gi = u.get_galaxy_instance()

invocation_id = args[1]

print('Invocation: ' + invocation_id)

invocation = gi.invocations.get_invocation_summary(invocation_id)

print(str(invocation))
