import ko from 'knockout';
import moment from 'moment';

class Event {
  constructor ({
    patient_number: patientNumber,
    patient_event_number: patientEventNumber,
    extra_notes: extraNotes,
    event_timestamp: eventTimestamp,
  }) {
    this.patientNumber = ko.observable(patientNumber);
    this.patientEventNumber = ko.observable(patientEventNumber);
    this.extraNotes = ko.observable(extraNotes);
    this.eventTimestamp = ko.observable(eventTimestamp);

    this.prettyTimestamp = ko.computed(
      () => moment(this.eventTimestamp()).format('MMM Do YYYY, h:mm a'),
    );
  }
}

export default Event;
