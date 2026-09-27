from locust import HttpUser, task, between

class ModelServiceUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task(3)
    def test_single_predict(self):
        self.client.post("/predict", json={"amount": 1500.0})

    @task(1)
    def test_batch_predict(self):
        payload = {
            "items": [{"amount": float(i * 10)} for i in range(1, 20)]
        }
        self.client.post("/predict/batch", json=payload)