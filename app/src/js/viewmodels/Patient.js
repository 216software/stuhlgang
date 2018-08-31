import ko from 'knockout';
import PatientDashboard from './PatientDashboard';
import PatientCreate from './PatientCreate';
import PatientManage from './PatientManage';
import PatientEvent from './PatientEvent';
import PatientNewEvent from './PatientNewEvent';
import store from '../services/store';
import { fetchPatientCollection } from '../services/api/patient';
import PatientModel from '../models/patient';

const getModelsFromResults = patients => patients.map(data => new PatientModel(data));

class Patient {
  constructor () {
    this.patients = ko.observableArray([]);
    this.events = ko.observableArray([]);

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

  // eslint-disable-next-line
  afterShow = () => {
    return this.fetchCollection();
  };
}

export default Patient;
