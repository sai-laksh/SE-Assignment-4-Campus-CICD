
from datetime import timedelta


def check_booking(start, end, existing, max_hours=3):
    if end <= start:
        return False

    if end - start > timedelta(hours=max_hours):
        return False

    for old_start, old_end in existing:
        if start < old_end and end > old_start:
            return False

    return True


def classify_sensor(value, threshold=50):
    if value is None:
        return "Invalid"

    return "Alert" if value >= threshold else "Normal"


def calculate_sla(created, hours=24):
    return created + timedelta(hours=hours)


def can_approve(role, restricted=False):
    if role == "administrator":
        return True

    if role == "department_approver" and not restricted:
        return True

    return False


def transition_ticket(current, new):
    transitions = {
        "Open": ["In Progress"],
        "In Progress": ["Resolved", "Open"],
        "Resolved": ["Closed", "In Progress"],
        "Closed": []
    }

    return new in transitions.get(current, [])


def process_sensor_event(event_id, seen_events, tickets, value):
    if event_id in seen_events:
        return False

    seen_events.add(event_id)

    if classify_sensor(value) == "Alert":
        tickets.append({
            "event_id": event_id,
            "priority": "High"
        })

    return True


def queue_sync(record, external_available, pending):
    if external_available:
        return "Synced"

    pending.append(record)
    return "Pending"


def validate_api_request(data):
    required = ["facility_id", "start", "end"]

    return all(
        key in data and data[key] is not None
        for key in required
    )


def migrate_records(old_records):
    migrated = []

    for record in old_records:
        updated = record.copy()
        updated.setdefault("status", "Open")
        updated["schema_version"] = 2
        migrated.append(updated)

    return migrated
