import store from './store';
import { removeItem } from './nativeStorage';

const logout = async () => {
  try {
    await removeItem('session');
    store.session(null);
    pager.navigate('login');
  } catch (error) {
    console.log('error', error);
  }
};

export default logout;
