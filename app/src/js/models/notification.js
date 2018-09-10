import ko from 'knockout';
import moment from 'moment';

class Notification {
  constructor ({
    id,
    data,
  }) {
    this.id = ko.observable(id);
    this.data = ko.observable(data);

    this.prettyTime = ko.computed(() => {
      const { hour, minute } = JSON.parse(this.data());
      const dateString = `2000-01-01 ${hour}:${minute}`;
      const m = moment(dateString, 'YYYY-MM-DD HH:mm');
      return m.format('hh:mm a');
    });
  }
}

export default Notification;
