from locust import HttpLocust, TaskSet, task
import random, string

class UserBehavior(TaskSet):
    @task(5)
    def l2s(self):
        response = self.client.get("/convert")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/convert/shorten",
                         {"url":"www.baidu.com"},
                         headers={'X-CSRFToken': csrftoken})

    @task(1)
    def s2l(self):
        """
        char_candidates = string.digits
        short_id = ''.join(
            random.choice(char_candidates)
            for i in range(2)
        )
        short_id = str(short_id).rjust(6,'0')
        url = '/convert/' + short_id
        self.client.get(url)
        """
        self.client.get("/convert/000003/")


# we have a HttpLocust class which represents a user
# where we define how long a simulated user should wait between executing tasks
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
