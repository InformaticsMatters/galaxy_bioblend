from galaxyclient import Utils
import sys

args = sys.argv

u = Utils()
gi = u.get_galaxy_instance()

invocation_id = args[1]

print('Invocation: ' + invocation_id)

inv = gi.invocations.show_invocation(invocation_id)

print(str(inv))
