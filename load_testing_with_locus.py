from locust import HttpUser, task

class APIUser(HttpUser):
    @task
    def get_resource(self):
        self.client.get("/api/resource")
