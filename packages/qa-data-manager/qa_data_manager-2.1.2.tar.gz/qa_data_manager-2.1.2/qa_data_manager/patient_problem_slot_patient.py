import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import PatientProblemSlotPatient


class GeneratePatientProblemSlotPatient:

    def __init__(self, problem, serivce, slot_patient):
        self._patient_problem = problem.get('id')
        self._service_id = serivce.get('id')
        self._slot_patient = slot_patient.get('id')

    def generate(self):
        problem_slot_patient = PatientProblemSlotPatient(created_at=datetime.datetime.now(),
                                                         patient_problem=self._patient_problem,
                                                         service_id=self._service_id,
                                                         slot_patient=self._slot_patient,
                                                         updated_at=datetime.datetime.now())

        problem_slot_patient.save()
        return model_to_dict(problem_slot_patient)
