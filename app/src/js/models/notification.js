import ko from 'knockout';
import moment from 'moment';

class Notification {
  constructor ({
    id,
    trigger: { every: { minute, hour } },
    data,
  }) {
    this.id = ko.observable(id);
    this.hour = ko.observable(hour);
    this.minute = ko.observable(minute);
    this.data = ko.observable(data);

    this.prettyTime = ko.computed(() => {
      const dateString = `2000-01-01 ${this.hour()}:${this.minute()}`;
      const m = moment(dateString, 'YYYY-MM-DD HH:mm');
      return m.format('hh:mm a');
    });
  }
}

export default Notification;
