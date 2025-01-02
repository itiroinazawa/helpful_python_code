from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_large_dataset(dataset_id):
    # Simulate processing
    print(f"Processing dataset {dataset_id}")

# Example Usage
process_large_dataset.delay(123)
