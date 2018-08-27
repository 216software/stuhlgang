import ko from 'knockout';
import BasePage from './BasePage';

class Dashboard extends BasePage {
  constructor () {
    super();
    this.patients = ko.observableArray([
      {
        id: 1,
        name: 'Billy Billson',
      },
      {
        id: 2,
        name: 'Johnny Johnson',
      },
    ]);

    this.patientUrl = ({ id }) => ko.computed(() => `/patients/${id}`, this);
  }

  isEmpty () {
    return !!(this.patients().length === 0);
  }
}

export default Dashboard;
