import store from '../services/store';
import { getItem } from '../services/nativeStorage';

class BasePage {
  constructor () {
    this.store = store;
  }

  initialize = async () => {
    try {
      const session = await getItem('session');
      this.store.session(session);
    } catch (error) {
      pager.navigate('login');
    }
  }
}

export default BasePage;
