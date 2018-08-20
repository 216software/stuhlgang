import ko from 'knockout';
import template from './template.html';

class Topbar {
  constructor () {
    this.activeNav = ko.observable('home');
    this.pages = [
      {
        name: 'home',
        title: 'Home',
        url: '/',
      },
      {
        name: 'page1',
        title: 'Page1',
        url: '/page1',
      },
    ];
  }
}

ko.components.register('topbar', {
  viewModel: Topbar,
  template,
});

export default Topbar;
