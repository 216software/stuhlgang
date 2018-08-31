import store from '../store';
import request from '../request';

const fetchEventCollection = ({ patientNumber, limit = 10, offset = 0 }) => {
  const params = new URLSearchParams(Object.entries({
    session_uuid: store.session(),
    patient_number: patientNumber,
    limit,
    offset,
  }));
  return request(`patient-events?${params}`);
};

const getEvent = (patientEventNumber) => {
  const params = new URLSearchParams({
    session_uuid: store.session(),
    patient_event_number: patientEventNumber,
  });
  return request(`patient-event?${params}`);
};

const createEvent = event => request('store-patient-event', {
  method: 'POST',
  body: JSON.stringify({
    ...event,
    session_uuid: store.session(),
  }),
});

const deleteEvent = eventId => request('delete-patient-event', {
  method: 'POST',
  body: JSON.stringify({
    patient_event_number: eventId,
    session_uuid: store.session(),
  }),
});

export {
  fetchEventCollection,
  getEvent,
  createEvent,
  deleteEvent,
};
