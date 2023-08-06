import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import PatientProblemDiscomfort


class GeneratePatientProblemDiscomfort:

    def __init__(self, consultation, patient_problem):
        self._consultation_id = consultation.get('id')
        self._consultation_type = 'slot'
        self._description = 'test description'
        self._level = 1
        self._patient_problem = patient_problem.get('id')

    def with_consultation_type(self):
        self._consultation_type = 'service_patient'
        return self

    def with_level(self, level):
        self._level = level
        return self

    def generate(self):
        problem_discomfort = PatientProblemDiscomfort(consultation_id=self._consultation_id,
                                                      consultation_type=self._consultation_type,
                                                      created_at=datetime.datetime.now(),
                                                      description=self._description,
                                                      level=self._level,
                                                      patient_problem=self._patient_problem,
                                                      updated_at=datetime.datetime.now())

        problem_discomfort.save()
        return model_to_dict(problem_discomfort)
