import ko from 'knockout';
import template from './template.html';
import { removeItem } from '../../services/nativeStorage';
import * as auth from '../../services/auth';
import store from '../../services/store';

class Topbar {
  constructor () {
    this.activeNav = ko.observable('home');

    this.pages = [
      {
        id: 'dashboard',
        title: 'Home',
        url: '/dashboard',
      },
    ];

    this.loggedIn = store.loggedIn;
  }

  logout = async () => {
    const response = await auth.logout();
    if (response.success) {
      await removeItem('session');
      store.session(null);
      store.loggedIn(false);
      pager.navigate('login');
    } else {
      store.error(response.message);
    }
  }
}

ko.components.register('topbar', {
  viewModel: Topbar,
  template,
});

export default Topbar;
