import ko from 'knockout';
import BasePage from './BasePage';
import { fetchEventCollection } from '../services/api/event';
import { deletePatient } from '../services/api/patient';
import store from '../services/store';
import Event from '../models/event';

const getModelsFromResults = events => events.map(data => new Event(data));

class PatientManage extends BasePage {
  constructor ({
    patients,
    events,
    parent,
    notifications,
  }) {
    super();
    this.patients = patients;
    this.parent = parent;
    this.events = events;
    this.notifications = notifications;

    this.myNotifications = ko.observableArray([]);

    // this will be set by pagerjs
    this.id = ko.observable(null);
    this.patient = ko.observable(null);

    this.limit = ko.observable(5); this.offset = ko.observable(0); this.total = ko.observable(0);

    this.canGoNext = ko.computed(() => (this.offset() + this.limit()) < this.total());
    this.canGoPrev = ko.computed(() => (this.offset() - this.limit()) >= 0);
  }

  fetchCollection = async () => {
    const patientNumber = this.patient().patientNumber();

    const response = await fetchEventCollection({
      patientNumber,
      limit: this.limit(),
      offset: this.offset(),
    });

    if (response.success) {
      this.events.removeAll();
      this.total(response.total_event_count);
      const events = getModelsFromResults(response.patient_events);
      events.forEach(event => this.events.push(event));
    } else {
      store.error(response.message);
      setTimeout(() => store.error(null), 3000);
    }
  }

  afterShow = async () => {
    await this.parent.afterShow();

    // find only notifications for *this* patientNumber
    this.myNotifications.removeAll();

    this.notifications().forEach((n) => {
      const data = n.data();
      console.log(`Data is ${data}`);

      const { patientNumber } = JSON.parse(data);
      console.log(`PatientNumber is ${patientNumber}`);

      if (Number(patientNumber) === Number(this.id())) {
        console.log(`Adding notification ${n.id()}`);
        this.myNotifications.push(n);
      }
    });

    /*
    const forThisPatient = this.notifications().filter(
      n => Number(n.data().patientNumber) === Number(this.id()),
    );
    this.myNotifications(forThisPatient);
    */

    this.reset();
    this.fetchCollection();
  };

  handleDelete = async () => {
    if (confirm('Are you sure you want to delete this patient?')) {
      const response = await deletePatient(this.id());

      if (response.success) {
        store.info(response.message);
        setTimeout(() => store.info(null), 3000);
        pager.navigate('patient');
      } else {
        store.error(response.message);
        setTimeout(() => store.error(null), 3000);
      }
    }
  };

  prevResults = () => {
    const newOffset = this.offset() - this.limit();

    if (newOffset >= 0) {
      this.offset(newOffset);
      this.fetchCollection();
    }
  }

  nextResults = () => {
    const newOffset = this.offset() + this.limit();

    if (newOffset < this.total()) {
      this.offset(newOffset);
      this.fetchCollection();
    }
  }

  reset () {
    this.limit(5);
    this.offset(0);
    this.total(0);

    const patient = this.patients().find(p => p.patientNumber() === Number(this.id()));
    this.patient(patient);
  }
}

export default PatientManage;
