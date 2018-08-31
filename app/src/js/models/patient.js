import ko from 'knockout';

class Patient {
  constructor ({
    patient_number: patientNumber,
    display_name: displayName,
    extra_notes: extraNotes,
    extra_data: extraData,
  }) {
    this.patientNumber = ko.observable(patientNumber);
    this.displayName = ko.observable(displayName);
    this.extraNotes = ko.observable(extraNotes);
    this.extraData = ko.observable(extraData);

    this.manageUrl = ko.computed(() => `/patient/manage?id=${this.patientNumber()}`);
    this.newEventUrl = ko.computed(() => `/patient/new_event?id=${this.patientNumber()}`);
  }
}

export default Patient;
