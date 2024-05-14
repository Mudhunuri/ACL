DOCTOR_ADMIN = 'doctor'
PATIENT_ADMIN = 'patient'

class Messages:
    SUCCESS = "success"
    DATA = "data"
    MESSAGE = "message"
    ERROR = "errors"
    DATA_IS_VALID = "Data is valid"

class DoctorApproval:
    ACCEPT = 'accepted'
    OPEN = 'open'
    DECLINE = 'declined'
    INPROGRESS = 'inprogress'
    CANCELLED = 'cancelled'

class Phases:
    DEMOGRAPHICS = 'Demographics'
    PREOPS = 'Pre-Op'
    PHASE1 = 'Phase 1'
    PHASE2 = 'Phase 2'
    PHASE3 = 'Phase 3'
    PHASE4 = 'Phase 4'
    COMPLETED = 'Completed'