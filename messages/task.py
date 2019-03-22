class Task:

    """ Task class """

    def __init__(self, task_id):
        super(Task, self).__init__()
        self.task_id = task_id
        self.is_terminated = False

    def is_terminated(self):
        return self.is_terminated
