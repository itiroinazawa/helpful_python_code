import time

RATE_LIMIT = 5
TIME_WINDOW = 60
requests_log = {}

def monitor_rate_limit(client_id):
    current_time = time.time()
    requests = requests_log.get(client_id, [])
    requests = [t for t in requests if current_time - t < TIME_WINDOW]
    if len(requests) >= RATE_LIMIT:
        return False  # Rate limit exceeded
    requests.append(current_time)
    requests_log[client_id] = requests
    return True
