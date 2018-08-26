import ko from 'knockout';
import template from './template.html';
import logout from '../../services/logout';

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
  }

  logout = () => logout()
}

ko.components.register('topbar', {
  viewModel: Topbar,
  template,
});

export default Topbar;
