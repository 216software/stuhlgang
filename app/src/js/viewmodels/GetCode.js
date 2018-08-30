import ko from 'knockout';
import BasePage from './BasePage';
import store from '../services/store';
import { requestCode } from '../services/api/auth';

class GetCode extends BasePage {
  constructor () {
    super();
    this.email = ko.observable('');
  }

  afterShow = () => {
    if (this.store.loggedIn()) {
      pager.navigate('patient');
    }
  }

  onSubmit = async () => {
    const response = await requestCode({ email: this.email() });

    if (response.success) {
      store.info(response.message);
      setTimeout(() => store.info(null), 3000);
      pager.navigate('login');
    }
  }
}

export default GetCode;
