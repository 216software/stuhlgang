import Home from './viewmodels/Home';
import Login from './viewmodels/Login';
import Dashboard from './viewmodels/Dashboard';
import store from './services/store';
import './components';

global.store = store;

class App {
  constructor () {
    this.homeViewModel = new Home();
    this.loginViewModel = new Login();
    this.dashboardViewModel = new Dashboard();

    this.session = store.session;
    this.error = store.error;
    this.info = store.info;
  }

  // eslint-disable-next-line
  initialize () {
    console.log('initialize app');
  }
}

export default App;
