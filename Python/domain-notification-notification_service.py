# Notification System

from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class SMSNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending SMS to {recipient}: {message}")
        # Actual SMS integration would go here
        return True

class PushNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending push notification to device {recipient}: {message}")
        # Actual push notification integration would go here
        return True

class EmailNotification(NotificationChannel):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Sending email to {recipient}: {message}")
        # Actual email integration would go here
        return True

class NotificationService:
    def __init__(self):
        self.channels = {
            'sms': SMSNotification(),
            'push': PushNotification(),
            'email': EmailNotification()
        }

    def send_notification(self, channel: str, recipient: str, message: str) -> bool:
        if channel not in self.channels:
            raise ValueError(f"Notification channel {channel} not supported")
            
        return self.channels[channel].send(recipient, message)