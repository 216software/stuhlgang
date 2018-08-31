import ko from 'knockout';
import BasePage from './BasePage';
import { getEvent, deleteEvent } from '../services/api/event';
import Event from '../models/event';

class PatientEvent extends BasePage {
  constructor ({ events, parent }) {
    super();
    this.events = events;
    this.parent = parent;
    this.eventId = ko.observable();
    this.event = ko.observable({});
  }

  afterShow = async () => {
    const response = await getEvent(this.eventId());

    if (response.success) {
      this.event(new Event(response.patient_event));
    } else {
      this.store.error(response.message);
      setTimeout(() => this.store.error(null), 3000);
    }
  };

  handleDelete = async () => {
    if (confirm('Are you sure you want to delete this event?')) {
      const response = await deleteEvent(this.eventId());

      if (response.success) {
        this.store.info(response.message);
        setTimeout(() => this.store.info(null), 3000);
        pager.navigate(`patient/manage?id=${this.event().patientNumber()}`);
      } else {
        this.store.error(response.message);
        setTimeout(() => this.store.error(null), 3000);
      }
    }
  };
}

export default PatientEvent;
