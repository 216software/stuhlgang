import ko from 'knockout';
import BasePage from './BasePage';

class ManageNotification extends BasePage {
  constructor ({ notifications }) {
    super();
    this.patientNumber = ko.observable();
    this.id = ko.observable();
    this.notification = ko.observable();
    this.notifications = notifications;
  }

  getNotification = () => new Promise((resolve) => {
    resolve(this.notifications().find(n => n.id() === Number(this.id())));
  });

  deleteNotification = () => {
    console.log(this.notification());
    console.log(this.notification().id());
    cordova.plugins.notification.local.cancel(Number(this.id()), () => {
      this.store.info('Deleted notification');
      setTimeout(() => this.store.info(null), 3000);

      pager.navigate(`patient/manage?id=${this.patientNumber()}`);
    });
  };

  afterShow = async () => {
    const notification = await this.getNotification();
    console.log('found');
    console.log(notification.id());
    this.notification(notification);
  };
}

export default ManageNotification;
