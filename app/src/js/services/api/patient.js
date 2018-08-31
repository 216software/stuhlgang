import store from '../store';
import request from '../request';

const fetchPatientCollection = () => {
  const params = new URLSearchParams(Object.entries({ session_uuid: store.session() }));
  return request(`patients-for-caretaker?${params}`);
};

const createPatient = patient => request('add-patient-for-caretaker', {
  method: 'POST',
  body: JSON.stringify({
    ...patient,
    session_uuid: store.session(),
  }),
});

const deletePatient = patientNumber => request('delete-patient', {
  method: 'POST',
  body: JSON.stringify({
    patient_number: patientNumber,
    session_uuid: store.session(),
  }),
});

export {
  fetchPatientCollection,
  createPatient,
  deletePatient,
};
