import ko from 'knockout';
import moment from 'moment';
import BasePage from './BasePage';
import { createEvent } from '../services/api/event';
import store from '../services/store';

class PatientNewEvent extends BasePage {
  constructor ({ patients, parent }) {
    super();
    this.patients = patients;
    this.parent = parent;

    this.date = ko.observable(moment().format('YYYY-MM-DD'));
    this.time = ko.observable(moment().format('HH:mm'));
    this.notes = ko.observable('');

    this.id = ko.observable(null);
    this.patient = ko.observable({}).extend({ notify: 'always' });
  }

  afterShow = async () => {
    await this.parent.afterShow();

    const patient = this.patients().find(p => p.patientNumber() === Number(this.id()));
    this.patient(patient);

    const now = moment();
    this.date(now.format('YYYY-MM-DD'));
    this.time(now.format('HH:mm'));
  };

  beforeHide = () => {
    this.notes('');
  };

  saveEvent = async () => {
    const patientNumber = this.patient().patientNumber();

    const dateTime = moment(`${this.date()} ${this.time()}`);

    const response = await createEvent({
      event_timestamp: dateTime.toISOString(),
      extra_notes: this.notes(),
      extra_data: {},
      patient_number: patientNumber,
    });

    if (response.success) {
      store.info(response.message);
      setTimeout(() => store.info(null), 3000);
      pager.navigate(`patient/manage?id=${patientNumber}`);
    } else {
      store.error(response.message);
      setTimeout(() => store.error(null), 3000);
    }
  };
}

export default PatientNewEvent;
