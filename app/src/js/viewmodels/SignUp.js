import ko from 'knockout';
import BasePage from './BasePage';
import { signup } from '../services/api/auth';

class SignUp extends BasePage {
  constructor () {
    super();
    this.displayName = ko.observable('');
    this.email = ko.observable('');
    this.tos = ko.observable(false);
  }

  handleSubmit = async () => {
    const response = await signup({
      displayName: this.displayName(),
      email: this.email(),
      tos: this.tos(),
    });

    if (response.success) {
      this.store.info(response.message);
      setTimeout(() => this.store.info(null), 3000);
      pager.navigate('login');
    } else {
      this.store.error(response.message);
      setTimeout(() => this.store.error(null), 3000);
    }
  }
}

export default SignUp;
