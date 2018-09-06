import moment from 'moment';
import Notification from '../models/notification';

const getIdAndIncrement = () => new Promise((resolve) => {
  // eslint-disable-next-line
  cordova.plugins.notification.local.getIds((ids) => {
    if (ids.length === 0) return 1;
    resolve(ids.sort((a, b) => a - b).pop() + 1);
  });
});

const getNotifications = () => new Promise((resolve) => {
  cordova.plugins.notification.local.getScheduled((notifications) => {
    resolve(notifications.map(nt => new Notification(nt)));
  });
});

const createNotification = ({
  title,
  text,
  hour,
  minute,
  patientNumber,
}) => new Promise(async (resolve) => {
  const nextId = await getIdAndIncrement();

  const dt = moment();
  dt.set('hours', hour);
  dt.set('minutes', minute);
  dt.set('secods', 0);

  cordova.plugins.notification.local.schedule({
    id: nextId,
    title,
    text,
    every: 'day',
    firstAt: dt.toDate(),
    data: { patientNumber, hour, minute },
  }, () => resolve(true));
});

const deleteNotification = id => new Promise((resolve) => {
  cordova.plugins.notification.local.cancel(id, () => resolve(true));
});

export {
  getNotifications,
  createNotification,
  deleteNotification,
};
