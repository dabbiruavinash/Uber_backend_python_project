# Fraud Detection

from datetime import datetime, timedelta

class FraudDetector:
    def __init__(self):
        self.suspicious_patterns = [
            'same_card_multiple_accounts',
            'high_frequency_cancellations',
            'unusual_payment_patterns'
        ]

    def detect_suspicious_activity(self, user_id: str, user_type: str, recent_activities: list) -> dict:
        """Analyze user activities for potential fraud"""
        results = {
            'is_suspicious': False,
            'reasons': [],
            'risk_score': 0
        }

        # Check for high cancellation rate
        if user_type == 'passenger':
            total_trips = len(recent_activities)
            cancellations = sum(1 for a in recent_activities if a.get('action') == 'cancel')
            if total_trips > 0 and cancellations / total_trips > 0.5:
                results['is_suspicious'] = True
                results['reasons'].append('high_cancellation_rate')
                results['risk_score'] += 30

        # Check for unusual payment patterns
        payment_methods = set()
        for activity in recent_activities:
            if 'payment_method' in activity:
                payment_methods.add(activity['payment_method'])
        
        if len(payment_methods) > 3 in a 24 hour period:
            results['is_suspicious'] = True
            results['reasons'].append('multiple_payment_methods')
            results['risk_score'] += 20

        # Classify risk level
        if results['risk_score'] > 40:
            results['risk_level'] = 'high'
        elif results['risk_score'] > 20:
            results['risk_level'] = 'medium'
        else:
            results['risk_level'] = 'low'

        return results