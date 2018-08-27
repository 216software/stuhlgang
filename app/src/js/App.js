import Login from './viewmodels/Login';
import GetCode from './viewmodels/GetCode';
import Dashboard from './viewmodels/Dashboard';
import store from './services/store';
import { verify } from './services/auth';
import { getItem } from './services/nativeStorage';
import './components';

global.store = store;

class App {
  constructor () {
    this.loginViewModel = new Login();
    this.dashboardViewModel = new Dashboard();
    this.getCodeViewModel = new GetCode();

    this.session = store.session;
    this.error = store.error;
    this.info = store.info;
  }

  // eslint-disable-next-line
  initialize () {
    this.verifySession();
  }

  getSession = async () => {
    try {
      const session = await getItem('session');
      return session;
    } catch (error) {
      return null;
    }
  }

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
