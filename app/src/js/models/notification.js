import ko from 'knockout';
import moment from 'moment';

/*
 * This is an example of the JSON representation of a notification
 *
[
  {
    "smallIcon":"res://icon",
    "title":"My first notification",
    "defaults":0,
    "vibrate":false,
    "foreground":true,
    "showWhen":true, "progressBar":{
      "enabled":false,
      "value":0
    },
    "launch":true,
    "lockscreen":true,
    "autoClear":true,
    "priority":1,
    "meta":{
      "version":"0.9-beta.2",
      "plugin":"cordova-plugin-local-notification"
    },
    "id":1,
    "number":0,
    "wakeup":true,
    "attachments":[],
    "silent":false,
    "text":"Thats pretty easy...",
    "groupSummary":false,
    "actions":[],
    "trigger":{
      "every":{
        "minute":2,
        "hour":15
      },
      "type":"calendar"
    },
    "led":true,
    "sound":true
  }
]
*/

class Notification {
  constructor ({
    id,
    trigger: { every: { minute, hour } },
  }) {
    this.id = ko.observable(id);
    this.hour = ko.observable(hour);
    this.minute = ko.observable(minute);
    this.data = ko.observable({});

    this.prettyTime = ko.computed(() => {
      const dateString = `2000-01-01 ${this.hour()}:${this.minute()}`;
      const m = moment(dateString, 'YYYY-MM-DD HH:mm');
      return m.format('hh:mm a');
    });
  }
}

export default Notification;
