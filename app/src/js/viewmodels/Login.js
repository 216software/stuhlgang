import ko from 'knockout';
import store from '../services/store';
import { getItem, setItem } from '../services/nativeStorage';
import request from '../services/request';

class Login {
  constructor () {
    this.email = ko.observable('');
    this.password = ko.observable('');
  }

  initialize = async () => {
    try {
      const session = await getItem('session');
      store.session(session);
    } catch (error) {
      console.log('no session');
    }
  }

  onSubmit = async () => {
    const response = await request('login', {
      method: 'POST',
      body: JSON.stringify({
        email_address: this.email(),
        password: this.password(),
      }),
    });

    if (response.success) {
      // store the session uuid
      store.session(response.session.session_uuid);
      await setItem('session', response.session.session_uuid);

      // display success message and clear after a few seconds
      store.error('');
      store.info('You have been logged in');
      setTimeout(() => {
        store.info('');
      }, 3000);

      pager.navigate('dashboard');
    } else {
      store.info('');
      store.error(response.message);
    }
  }
}

export default Login;
