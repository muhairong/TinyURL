from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.index()

    @task(1)
    def index(self):
        self.client.get("/convert")

    @task(2)
    def l2s(self):
        response = self.client.get("/convert")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/convert/shorten",
                         {"url":"www.baidu.com"},
                         headers={'X-CSRFToken': csrftoken})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
