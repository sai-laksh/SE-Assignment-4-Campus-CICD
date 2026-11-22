
import unittest
from datetime import datetime, timedelta

from campus_rules import (
    check_booking,
    classify_sensor,
    calculate_sla,
    can_approve,
    transition_ticket,
    process_sensor_event,
    queue_sync,
    validate_api_request,
    migrate_records
)


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.start = datetime(2026, 11, 22, 10, 0)

    def test_valid_booking(self):
        self.assertTrue(
            check_booking(
                self.start,
                self.start + timedelta(hours=2),
                []
            )
        )

    def test_booking_overlap(self):
        existing = [
            (self.start, self.start + timedelta(hours=2))
        ]
        self.assertFalse(
            check_booking(
                self.start + timedelta(hours=1),
                self.start + timedelta(hours=3),
                existing
            )
        )

    def test_maximum_duration(self):
        self.assertTrue(
            check_booking(
                self.start,
                self.start + timedelta(hours=3),
                []
            )
        )

    def test_sensor_threshold(self):
        self.assertEqual(classify_sensor(50), "Alert")
        self.assertEqual(classify_sensor(49), "Normal")

    def test_sla_deadline(self):
        deadline = calculate_sla(self.start)
        self.assertEqual(deadline, self.start + timedelta(hours=24))

    def test_unauthorized_approval(self):
        self.assertFalse(can_approve("student", True))


class IntegrationTests(unittest.TestCase):

    def test_sensor_event_creates_ticket(self):
        seen = set()
        tickets = []

        result = process_sensor_event(
            "E101", seen, tickets, 60
        )

        self.assertTrue(result)
        self.assertEqual(len(tickets), 1)

    def test_duplicate_event_not_processed(self):
        seen = {"E101"}
        tickets = []

        result = process_sensor_event(
            "E101", seen, tickets, 60
        )

        self.assertFalse(result)
        self.assertEqual(len(tickets), 0)

    def test_external_failure_preserves_record(self):
        pending = []
        record = {"ticket_id": 10}

        result = queue_sync(record, False, pending)

        self.assertEqual(result, "Pending")
        self.assertIn(record, pending)

    def test_api_request_validation(self):
        request = {
            "facility_id": 1,
            "start": "10:00",
            "end": "11:00"
        }

        self.assertTrue(validate_api_request(request))


class RegressionTests(unittest.TestCase):

    def test_adjacent_bookings_are_allowed(self):
        first_start = datetime(2026, 11, 22, 10, 0)
        first_end = datetime(2026, 11, 22, 11, 0)

        second_start = first_end
        second_end = datetime(2026, 11, 22, 12, 0)

        self.assertTrue(
            check_booking(
                second_start,
                second_end,
                [(first_start, first_end)]
            )
        )

    def test_restricted_approval(self):
        self.assertFalse(can_approve("department_approver", True))

    def test_invalid_ticket_transition(self):
        self.assertFalse(transition_ticket("Open", "Closed"))

    def test_valid_ticket_transition(self):
        self.assertTrue(transition_ticket("Open", "In Progress"))

    def test_migration_preserves_old_records(self):
        old = [{"ticket_id": 1, "description": "Repair"}]

        new = migrate_records(old)

        self.assertEqual(new[0]["ticket_id"], 1)
        self.assertEqual(new[0]["schema_version"], 2)
        self.assertEqual(new[0]["status"], "Open")


if __name__ == "__main__":
    unittest.main()
