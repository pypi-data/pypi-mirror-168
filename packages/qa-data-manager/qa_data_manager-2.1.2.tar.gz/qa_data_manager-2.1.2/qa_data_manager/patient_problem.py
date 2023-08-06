import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import PatientProblems


class GeneratePatientProblem:

    def __init__(self, patient):
        self._days = 1
        self._patient = patient.get('id')
        self._title = 'kiss my ass'

    def with_days(self, days):
        self._days = days
        return self

    def with_title(self, title):
        self._title = title
        return self

    def generate(self):
        patient_problem = PatientProblems(created_at=datetime.datetime.now(),
                                          days=self._days,
                                          patient=self._patient,
                                          title=self._title,
                                          updated_at=datetime.datetime.now())

        patient_problem.save()
        return model_to_dict(patient_problem)
