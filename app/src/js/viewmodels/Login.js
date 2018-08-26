import ko from 'knockout';
import BasePage from './BasePage';
import { setItem } from '../services/nativeStorage';
import { login } from '../services/auth';

class Login extends BasePage {
  constructor () {
    super();
    this.email = ko.observable('');
    this.password = ko.observable('');
  }

  afterShow = () => {
    if (this.store.loggedIn()) {
      pager.navigate('dashboard');
    }
  }

  onSubmit = async () => {
    const response = await login({
      email: this.email(),
      password: this.password(),
    });

    if (response.success) {
      // store the session uuid
      this.store.session(response.session.session_uuid);
      this.store.loggedIn(true);
      await setItem('session', response.session.session_uuid);

      // display success message and clear after a few seconds
      this.store.error('');
      this.store.info('You have been logged in');
      setTimeout(() => {
        this.store.info('');
      }, 3000);

      pager.navigate('dashboard');
    } else {
      this.store.info('');
      this.store.error(response.message);
    }
  }
}

export default Login;
