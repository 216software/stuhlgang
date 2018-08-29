import ko from 'knockout';
import BasePage from './BasePage';
import { createPatient } from '../services/api/patient';
import store from '../services/store';

class PatientCreate extends BasePage {
  constructor () {
    super();
    this.displayName = ko.observable('');
    this.extraNotes = ko.observable('');
    this.dob = ko.observable('');
  }

  refresh = () => {
    this.displayName('');
    this.extraNotes('');
    this.dob('');
  };

  createPatient = async () => {
    const response = await createPatient({
      display_name: this.displayName(),
      extra_notes: this.extraNotes(),
      extra_data: JSON.stringify({
        dob: this.dob(),
      }),
    });

    if (response.success) {
      store.info(response.message);
      setTimeout(() => store.info(null), 3000);
      this.refresh();
      pager.navigate('patient');
    } else {
      store.error(response.message);
      setTimeout(() => store.error(null), 3000);
    }
  };

  cancel = () => {
    this.refresh();
    pager.navigate('patient');
  };
}

export default PatientCreate;
