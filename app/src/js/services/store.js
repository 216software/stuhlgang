import ko from 'knockout';

const store = {
  error: ko.observable(),
  info: ko.observable(),
  session: ko.observable(),
  loggedIn: ko.observable(false),
};

export default store;
