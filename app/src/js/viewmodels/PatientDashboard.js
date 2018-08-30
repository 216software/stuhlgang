import BasePage from './BasePage';

class PatientDashboard extends BasePage {
  constructor ({ patients, parent }) {
    super();
    this.patients = patients;
    this.parent = parent;
  }

  isEmpty () {
    return !!(this.patients().length === 0);
  }

  afterShow = () => {
    this.parent.afterShow();
  };
}

export default PatientDashboard;
