import Home from './viewmodels/Home';
import './components';

class App {
  constructor () {
    console.debug("Inside constructor for App...");
    this.homeViewModel = new Home();
  }
}

export default App;
