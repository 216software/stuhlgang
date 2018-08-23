import Home from './viewmodels/Home';
import { getItem, setItem, removeItem } from './services/nativeStorage';
import './components';

class App {
  constructor () {
    this.homeViewModel = new Home();
  }

  initialize = async () => {
    await setItem('session', 'foobar');

    let result = await getItem('session');
    console.log(result);

    await removeItem('session');

    try {
      result = await getItem('session');
    } catch (error) {
      result = null;
    }

    console.log(result);
  }
}

export default App;
