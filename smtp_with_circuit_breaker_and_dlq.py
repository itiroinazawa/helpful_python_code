import smtplib
from email.message import EmailMessage
import queue
import time

# Dead Letter Queue (DLQ)
dlq = queue.Queue()

def send_email_notification(sender_email, sender_password, recipient_email, subject, body, smtp_server='smtp.gmail.com', smtp_port=587, max_retries=3):
    """
    Sends an email notification with retry logic and DLQ handling.

    Args:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password or app-specific password.
        recipient_email (str): Recipient's email address.
        subject (str): Subject of the email.
        body (str): Body of the email.
        smtp_server (str, optional): SMTP server. Defaults to 'smtp.gmail.com'.
        smtp_port (int, optional): SMTP port. Defaults to 587.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.
    """
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Create the email
            msg = EmailMessage()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.set_content(body)

            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Start TLS encryption
                server.login(sender_email, sender_password)  # Login to the SMTP server
                server.send_message(msg)  # Send the email

            print("Email sent successfully.")
            return

        except Exception as e:
            print(f"Failed to send email: {e}")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff

    # If retries are exhausted, add to Dead Letter Queue
    print("Max retries reached. Adding to DLQ.")
    dlq.put({
        'sender_email': sender_email,
        'recipient_email': recipient_email,
        'subject': subject,
        'body': body,
        'error': str(e)
    })

class CircuitBreaker:
    """Simple circuit breaker implementation."""
    def __init__(self, failure_threshold=5, recovery_time=60):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = None

    def allow_request(self):
        if self.failure_count < self.failure_threshold:
            return True
        elif self.last_failure_time and (time.time() - self.last_failure_time) > self.recovery_time:
            self.reset()
            return True
        return False

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

    def reset(self):
        self.failure_count = 0
        self.last_failure_time = None

# Initialize the circuit breaker
circuit_breaker = CircuitBreaker()

# Example usage
if __name__ == "__main__":
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    recipient_email = "recipient_email@gmail.com"
    subject = "Test Notification"
    body = "This is a test email notification from the API."

    if circuit_breaker.allow_request():
        try:
            send_email_notification(sender_email, sender_password, recipient_email, subject, body)
        except Exception as e:
            print(f"Error sending email: {e}")
            circuit_breaker.record_failure()
    else:
        print("Circuit breaker is open. Request denied.")
