import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Tracks


class GenerateTracks:

    def __init__(self, patient_problem):
        self._entity_id = patient_problem.get('id')
        self._entity_type = 'patient_problem'
        self._flow = None
        self._status = 'auto'

    def with_entity_type_slot_doctor(self):
        self._entity_type = 'slot_doctor'
        return self

    def with_status_appointed_offline_reception(self):
        self._status = 'appointed_offline_reception'
        return self

    def with_status_approved(self):
        self._status = 'approved'
        return self

    def with_status_canceled(self):
        self._status = 'canceled'
        return self

    def with_status_closed(self):
        self._status = 'closed'
        return self

    def with_status_diagnostics_assigned(self):
        self._status = 'diagnostics_assigned'
        return self

    def with_status_primary_appointment(self):
        self._status = 'primary_appointment'
        return self

    def with_status_pending(self):
        self._status = 'pending'
        return self

    def with_status_repeated_appointment(self):
        self._status = 'repeated_appointment'
        return self

    def with_status_second_opinion(self):
        self._status = 'second_opinion'
        return self

    def with_status_transcript_of_analyzes(self):
        self._status = 'transcript_of_analyzes'
        return self

    def with_status_treatment_completed(self):
        self._status = 'treatment_completed'
        return self

    def with_status_treatment_prescribed(self):
        self._status = 'treatment_prescribed'
        return self

    def with_status_wait_payment(self):
        self._status = 'wait_payment'
        return self

    def generate(self):
        tracks = Tracks(created_at=datetime.datetime.now(),
                        entity_id=self._entity_id,
                        entity_type=self._entity_type,
                        flow=self._flow,
                        status=self._status,
                        updated_at=datetime.datetime.now())

        tracks.save()
        return model_to_dict(tracks)
