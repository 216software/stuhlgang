import ko from 'knockout';
import BasePage from './BasePage';
import { createNotification } from '../services/localNotification';

const getIdAndIncrement = () => new Promise((resolve) => {
  // eslint-disable-next-line
  cordova.plugins.notification.local.getIds((ids) => {
    if (ids.length === 0) return 1;
    resolve(ids.sort((a, b) => a - b).pop() + 1);
  });
});

class CreateNotification extends BasePage {
  constructor ({ patients }) {
    super();
    this.patients = patients;
    this.id = ko.observable();
    this.patient = ko.observable();
    this.time = ko.observable();
    getIdAndIncrement();
  }

  createNotification = async () => {
    const timeParts = this.time().split(':');
    const hour = Number(timeParts[0]);
    const minute = Number(timeParts[1]);
    const displayName = this.patient().displayName();

    console.log('About to create notification');

    await createNotification({
      title: 'Time to poop!',
      text: `It's time for ${displayName} to poop.`,
      hour,
      minute,
      patientNumber: Number(this.id()),
    });

    console.log('Notification created');

    this.store.info('Notification Scheduled!');
    setTimeout(() => this.store.info(null), 3000);

    pager.navigate(`patient/manage?id=${this.id()}`);
  };

  afterShow = () => {
    const patient = this.patients().find(p => p.patientNumber() === Number(this.id()));
    this.patient(patient);
  };
}

export default CreateNotification;
