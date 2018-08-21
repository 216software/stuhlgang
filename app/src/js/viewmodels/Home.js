class Home {
  constructor () {
    this.title = 'Home Page';
    this.type = 'Homer';
  }

  initializePage1 = () => {
    console.debug('In initialize_page_1...', this.title);
  }

  initializeHome = () => {
    console.debug('In initialize_home...', this.type);
  }
}

export default Home;
