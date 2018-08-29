import store from '../services/store';

class BasePage {
  constructor () {
    this.store = store;

    this.initialize = this.initialize.bind(this);
  }

  initialize () {
    if (this.afterShow) this.afterShow();
  }
}

export default BasePage;
