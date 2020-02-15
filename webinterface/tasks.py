class TasksClass():

    def __init__(self, count):
        self.count = count

    def update_forecast(self):
        self.count += 3
        print('hi:', self.count)
