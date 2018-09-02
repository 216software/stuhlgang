import ko from 'knockout';
import CreateNotification from './CreateNotification';
import ManageNotification from './ManageNotification';
import PatientDashboard from './PatientDashboard';
import PatientCreate from './PatientCreate';
import PatientManage from './PatientManage';
import PatientEvent from './PatientEvent';
import PatientNewEvent from './PatientNewEvent';
import store from '../services/store';
import { fetchPatientCollection } from '../services/api/patient';
import PatientModel from '../models/patient';
import NotificationModel from '../models/notification';

const getModelsFromResults = patients => patients.map(data => new PatientModel(data));

class Patient {
  constructor () {
    this.patients = ko.observableArray([]);
    this.events = ko.observableArray([]);
    this.notifications = ko.observableArray([]);

    this.createNotificationViewModel = new CreateNotification({
      patients: this.patients,
      parent: this,
    });

    this.manageNotificationViewModel = new ManageNotification({
      notifications: this.notifications,
      parent: this,
    });

    this.patientDashboardViewModel = new PatientDashboard({
      patients: this.patients,
      parent: this,
    });

    this.patientCreateViewModel = new PatientCreate({
      patients: this.patients,
      parent: this,
    });

    this.patientManageViewModel = new PatientManage({
      patients: this.patients,
      events: this.events,
      notifications: this.notifications,
      parent: this,
    });

    this.patientNewEventViewModel = new PatientNewEvent({
      patients: this.patients,
      parent: this,
    });

    this.patientEventViewModel = new PatientEvent({
      events: this.events,
      parent: this,
    });
  }

  fetchCollection = async () => {
    const response = await fetchPatientCollection();

    const promise = new Promise((resolve, reject) => {
      if (response.success) {
        this.patients.removeAll();
        const patients = getModelsFromResults(response.patients);
        patients.forEach(patient => this.patients.push(patient));
        resolve(this.patients);
      } else {
        store.error(response.message);
        setTimeout(() => store.error(null), 3000);
        reject(response.message);
      }
    });

    return promise;
  };

  getNotifications = () => new Promise((resolve) => {
    this.notifications.removeAll();
    cordova.plugins.notification.local.getScheduled((nots) => {
      nots.forEach(nt => this.notifications.push(new NotificationModel(nt)));
      resolve(this.notifications);
    });
  });

  // eslint-disable-next-line
  afterShow = async () => {
    await this.getNotifications();
    return this.fetchCollection();
  };
}

export default Patient;
