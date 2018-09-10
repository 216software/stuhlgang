import $ from 'jquery';
import Login from './viewmodels/Login';
import GetCode from './viewmodels/GetCode';
import SignUp from './viewmodels/SignUp';
import Patient from './viewmodels/Patient';
import store from './services/store';
import { verify } from './services/api/auth';
import { getItem } from './services/nativeStorage';

class App {
  constructor () {
    this.loginViewModel = new Login();
    this.getCodeViewModel = new GetCode();
    this.signUpViewModel = new SignUp();
    this.patientViewModel = new Patient();

    this.session = store.session;
    this.error = store.error;
    this.info = store.info;
  }

  // eslint-disable-next-line
  initialize () {
    // Bloody hack to make navbar close after links clicked.
    $(document).on('click', '.sg-nav-link', () => {
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
