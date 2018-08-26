import store from '../services/store';

class BasePage {
  constructor () {
    this.store = store;
  }

  initialize = async () => {
    if (this.afterShow) this.afterShow();
  }
}

export default BasePage;
