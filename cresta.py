from typing import List, Dict

# You are tasked with implementing a simple job dispatcher that distributes incoming jobs to a pool of executors (i.e., 
# workers). Each job is represented as an integer (its ID), and executors are dynamically added and removed during runtime.
# Executors will not actually do any work for the purpose of this interview, simply track any outstanding jobs to be completed.

class Executor:
    def init(self, id):
        self.id = id
        self.job_tasks = []

    def assign_job(self, job_id: int):
        # assign a job to this executor
        self.job_tasks.append(job_id)
        pass

    def execute_next_job(self):
        # complete a job
        if len(self.job_tasks) == 0:
            return

        print(self.job_tasks[0])
        self.job_tasks = self.job_tasks[1:]
        pass

class JobDispatcher:
    def init(self):
        self.pool = {}

    def add_executor(self, executor: Executor):
        # add an executor to the pool
        self.pool[executor.id] = executor
        pass

    def remove_executor(self, executor_id: str):
        # remove executor from the pool
        tmp_exec = self.pool[executor_id]

        self.pool.pop(executor_id, None)

        for id in tmp_exec.job_tasks:
            self.dispatch(id)
        
        pass

    def dispatch(self, job_id: int):
        # assign the job to one of the available executors
        min_task_length = 10000 # the most number of tasks
        free_executor = None

        for k, v in self.pool.items():
            if len(v.job_tasks) < min_task_length:
                min_task_length = len(v.job_tasks)
                free_executor = v

        if free_executor:
            free_executor.assign_job(job_id)

        pass

    def get_state(self) -> Dict[str, List[int]]:
        repr_dict = dict()
        for exec_id, exec in self.pool.items():
            repr_dict[exec_id] = [id for id in exec.job_tasks]
        # return a dict of executor_id -> list of assigned job IDs
        return repr_dict


global_job_dispatcher = JobDispatcher()

executor_1 = Executor(1)
executor_2 = Executor(2)

global_job_dispatcher.add_executor(executor_1)
global_job_dispatcher.add_executor(executor_2)

global_job_dispatcher.dispatch(1)
global_job_dispatcher.dispatch(2)
global_job_dispatcher.dispatch(3)
global_job_dispatcher.remove_executor(2)
global_job_dispatcher.dispatch(4)

print(global_job_dispatcher.get_state())
