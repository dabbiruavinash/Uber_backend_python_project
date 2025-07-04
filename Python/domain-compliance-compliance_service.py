# Compliance Management

from datetime import datetime, timedelta

class ComplianceChecker:
    INDIA_SPECIFIC_REGULATIONS = {
        'max_driving_hours': 9,
        'mandatory_break_after_hours': 4.5,
        'documents_required': ['license', 'rc', 'insurance', 'puc']
    }

    def check_driver_compliance(self, driver, trips_last_24_hours):
        """Check if driver meets all regulatory requirements"""
        violations = []
        
        # Check documents
        for doc in self.INDIA_SPECIFIC_REGULATIONS['documents_required']:
            if doc not in driver.documents:
                violations.append(f"missing_{doc}")

        # Check driving hours
        total_driving_hours = sum(trip['duration_hours'] for trip in trips_last_24_hours)
        if total_driving_hours > self.INDIA_SPECIFIC_REGULATIONS['max_driving_hours']:
            violations.append("exceeded_max_driving_hours")

        # Check breaks
        continuous_driving = 0
        for trip in sorted(trips_last_24_hours, key=lambda x: x['start_time']):
            if continuous_driving + trip['duration_hours'] > self.INDIA_SPECIFIC_REGULATIONS['mandatory_break_after_hours']:
                violations.append("missed_mandatory_break")
                break
            continuous_driving += trip['duration_hours']
            if trip.get('break_after'):
                continuous_driving = 0

        return {
            'is_compliant': len(violations) == 0,
            'violations': violations,
            'last_checked': datetime.utcnow()
        }