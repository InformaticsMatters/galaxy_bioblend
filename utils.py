from bioblend import galaxy
import time
from yaml import load, Loader

class Utils:

    gi = None
    config = load(file('galaxy-config.yml', 'r'), Loader=Loader)

    def __init__(self):
        url = self.config['galaxy_url']
        print('Using Galaxy at ' + url)
        self.gi = galaxy.GalaxyInstance(url=url, key=self.config['galaxy_key'])

    def wait_on_state(self, func, prop='state', states=['ok'], period=5):
        status = func()[prop]
        while status not in states:
            print("waiting ...")
            time.sleep(period)
            status = func()[prop]
        return status

    def get_workflows(self):
        """
        List the available workflows
        :return:
        """
        return self.gi.workflows.get_workflows()

    def show_workflow(self, id):
        return self.gi.workflows.show_workflow(id)

    def get_invocation(self, workflow_id, invocation_id):
        return self.gi.workflows.show_invocation(workflow_id, invocation_id)

    def get_job_ids(self, invocation):
        ids = []
        for step in invocation['steps']:
            id = step['job_id']
            if id != None:
                ids.append(id)
        return ids

    def are_jobs_ok(self, job_ids):
        for job_id in job_ids:
            state = self.gi.jobs.get_state(job_id)
            if state != 'ok':
                return False
        return True

    def wait_on_jobs(self, job_ids, period=5):
        while not self.are_jobs_ok(job_ids):
            print('Waiting for jobs ...')
            time.sleep(period)

    def get_dataset_ids_from_history(self, history):
        ids = []
        for element in history:
            if element['history_content_type'] == 'dataset' and element['deleted'] == False:
                ids.append(element['dataset_id'])
        return ids

    def setup_history(self, history_name, inputs):
        history = self.gi.histories.create_history(history_name)
        history_id = history['id']
        print('Created history: ' + history_id + ' ' + history_name)
        # print('History: ' + str(initial_history))

        # upload files to history
        print('Uploading inputs')
        datamap = dict()
        for input in inputs:
            dataset = self.gi.tools.upload_file(input['file'], history_id, file_type=input['file_type'])
            datamap[input['id']] = { 'src':'hda', 'id':dataset['outputs'][0]['id'] }
            print('Uploaded input "' + input['file'] + '"')

        return history, datamap


    def run_workflow(self, workflow, history, datamap, output_dir):
        workflow_id = workflow['id']
        history_id = history['id']
        print('Executing workflow "' + workflow['name'] + '" in history "' + history['name'] + '"')

        start = time.time()

        pre_exec_datasets = self.gi.histories.show_history(history_id, contents=True)

        initial_invocation = self.gi.workflows.run_workflow(workflow_id, dataset_map=datamap,  history_id=history_id)
        invocation_id = initial_invocation['id']
        print('Invocation ID: ' +  invocation_id)

        status = self.wait_on_state(lambda: self.get_invocation(workflow_id, invocation_id), states='scheduled')
        print("Workflow scheduled")

        job_ids = self.get_job_ids(initial_invocation)
        print('Job IDs: ' + str(job_ids))

        self.wait_on_jobs(job_ids)
        print('Jobs completed')

        final_invocation = self.get_invocation(workflow_id, invocation_id)
        print(str(final_invocation))
        post_exec_datasets = self.gi.histories.show_history(history_id, contents=True)

        dataset_ids_before_exec = self.get_dataset_ids_from_history(pre_exec_datasets)
        dataset_ids_after_exec = self.get_dataset_ids_from_history(post_exec_datasets)
        dataset_ids_added_by_exec = list(dataset_ids_after_exec)
        # print('IDs before exec:   ' + str(datasets_ids_before_exec))
        # print('IDs after exec:    ' + str(datasets_ids_after_exec))

        for id in dataset_ids_before_exec:
            dataset_ids_added_by_exec.remove(id)

        print(str(len(dataset_ids_added_by_exec)) + ' datasets added by execution')

        count = 0
        for id in dataset_ids_added_by_exec:
            print('Handling output ' + id)
            dataset = self.gi.datasets.show_dataset(id)
            count += 1
            filename = output_dir + '/' + dataset['name'] + '.' + dataset['extension']
            print('Downloading ' + str(count) + ' ' + filename + " state is " + dataset['state'])
            self.gi.datasets.download_dataset(id, filename, use_default_filename=False)

        finish = time.time()
        print("Done in " + str(finish - start) + 'secs')

