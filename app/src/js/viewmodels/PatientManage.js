import ko from 'knockout';
import BasePage from './BasePage';

class PatientManage extends BasePage {
  constructor ({ patients, parent }) {
    super();
    this.patients = patients;
    this.parent = parent;

    // this will be set by pagerjs
    this.id = ko.observable(null);

    // this gets set in afterShow
    this.patient = ko.observable({});
  }

  afterShow = async () => {
    await this.parent.afterShow();

    const patient = this.patients().find(p => p.patientNumber() === Number(this.id()));
    this.patient(patient);
  };
}

export default PatientManage;
