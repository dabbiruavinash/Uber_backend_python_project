# Test Notification 

import unittest
from domain.notification.notification_service import NotificationService, SMSNotification, PushNotification

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.service = NotificationService()
        self.sms = SMSNotification()
        self.push = PushNotification()
        self.service.register_channel("sms", self.sms)
        self.service.register_channel("push", self.push)

    def test_sms_notification(self):
        result = self.sms.send("+919876543210", "Your ride is confirmed")
        self.assertTrue(result)

    def test_push_notification(self):
        result = self.push.send("device123", "Driver is arriving in 5 mins")
        self.assertTrue(result)

    def test_service_dispatch(self):
        result = self.service.send_notification("sms", "+919876543210", "Test SMS")
        self.assertTrue(result)
        
        result = self.service.send_notification("push", "device123", "Test Push")
        self.assertTrue(result)

    def test_invalid_channel(self):
        with self.assertRaises(ValueError):
            self.service.send_notification("email", "test@example.com", "Test")

if __name__ == '__main__':
    unittest.main()