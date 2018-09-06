import $ from 'jquery';
import 'bootstrap';
import Login from './viewmodels/Login';
import GetCode from './viewmodels/GetCode';
import Patient from './viewmodels/Patient';
import SignUp from './viewmodels/SignUp';
import store from './services/store';
import { verify } from './services/api/auth';
import { getItem } from './services/nativeStorage';
import './components';

global.store = store;

class App {
  constructor () {
    this.loginViewModel = new Login();
    this.getCodeViewModel = new GetCode();
    this.patientViewModel = new Patient();
    this.signUpViewModel = new SignUp();

    this.session = store.session;
    this.error = store.error;
    this.info = store.info;
  }

  // eslint-disable-next-line
  initialize () {
    // Bloody hack to make navbar close after links clicked.
    $(document).on('click', '.sg-nav-link', (event) => {
      $('#navbarSupportedContent').collapse('hide');
    });

    this.verifySession();
  }

  goToPatients = () => {
    pager.navigate('patient');
  };

  getSession = async () => {
    try {
      const session = await getItem('session');
      return session;
    } catch (error) {
      return null;
    }
  };

  verifySession = async () => {
    const session = await this.getSession();
    this.session(session);

    if (session) {
      const response = await verify({ session: this.session() });
      if (response.success) {
        store.loggedIn(true);
        return;
      }
    }

    pager.navigate('login');
  };
}

export default App;
