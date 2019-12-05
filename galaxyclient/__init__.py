from bioblend import galaxy
from yaml import load, Loader
import time

config = load(file('galaxy-config.yml', 'r'), Loader=Loader)
gi = galaxy.GalaxyInstance(url=config['galaxy_url'], key=config['galaxy_key'])

class Workflow:

    def __init__(self, history_name, workflow_id):
        self.history_name = history_name
        self.workflow_id = workflow_id
        history = gi.histories.create_history(self.history_name)
        self.history_id = history['id']
        print('Created history: ' + self.history_id + ' ' + self.history_name)

    def upload_inputs(self, inputs):
        # upload files to history
        print('Uploading inputs')
        inputsmap = dict()
        count = 0
        for input in inputs:
            dataset = gi.tools.upload_file(input['file'], self.history_id, file_type=input['file_type'])
            inputsmap[str(count)] = { 'src':'hda', 'id':dataset['outputs'][0]['id'] }
            print('Uploaded input "' + input['file'] + '"')
            count += 1

        return inputsmap

    def invoke_workflow(self, inputsmap, paramsmap):
        """
        Invoke the workflow with the given inputs and parameters

        :param inputsmap:
        :param paramsmap:
        :return:
        """

        invocation = gi.workflows.invoke_workflow(self.workflow_id, inputs=inputsmap, params=paramsmap, history_id=self.history_id)
        self.invocation_id = invocation['id']
        return invocation

    def wait_for_invocation(self, states=['scheduled','failed'], period=5):
        """
        Wait for the invocation to get the particular states

        :param states: Array of states to accept. Default is scheduled or failed
        :param period: Delay between testing the state. Default is 5s.
        :return:
        """
        invocation = gi.invocations.show_invocation(self.invocation_id)
        state = invocation['state']
        while state not in states:
            print('Invocation state is ' + state + ' ...')
            time.sleep(period)
            invocation = gi.invocations.show_invocation(self.invocation_id)
            state = invocation['state']
        print('Invocation state is ' + state)
        return invocation

    def wait_for_workflow_to_complete(self, states=['scheduled','failed'], period=5):

        invocation = gi.invocations.show_invocation(self.invocation_id)
        state = invocation['state']
        while state not in states:
            print('Invocation state is ' + state + ' ...')
            time.sleep(period)
            invocation = gi.invocations.show_invocation(self.invocation_id)
            state = invocation['state']

        if state == 'failed':
            print('Workflow failed: ' + str(invocation))
            raise

        print("Workflow scheduled")

        while True:
            summary = gi.invocations.get_invocation_summary(self.invocation_id)
            states = summary['states']
            print('States: ' + str(states) + ' ...')
            all_ok = True

            if 'new' in states and states['new'] > 0:
                all_ok = False
            elif 'running' in states and states['running'] > 0:
                all_ok = False
            elif 'queued' in states and states['queued'] > 0:
                all_ok = False

            if all_ok:
                #print(str(summary))
                print('States complete')
                return states

            time.sleep(period)

        print("Workflow complete")


    def download_outputs(self, output_dir):
        """
        Download the outputs of an invocation. To be downloaded the output must be marked as a workflow output (starred)
        and have the required name of the output file specified as the label for the output.
        Note: Output Collections are not yet supported.

        :param output_dir: Where to download the files to
        :return: The number of datasets downloaded
        """

        invocation = gi.invocations.show_invocation(self.invocation_id)
        outputs = invocation['outputs']
        count = 0
        for name in outputs:
            print('Downloading ' + name)
            output = outputs[name]
            dataset_id = output['id']
            gi.datasets.download_dataset(dataset_id, output_dir + '/' + name, use_default_filename=False)
            count += 1

        return count

class Utils:

    def get_galaxy_instance(self):
        return gi

