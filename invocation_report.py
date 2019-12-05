from galaxyclient import Utils
import sys

args = sys.argv

u = Utils()
gi = u.get_galaxy_instance()

invocation_id = args[1]

print('Invocation: ' + invocation_id)

report = gi.invocations.get_invocation_report(invocation_id)

print(str(report))
