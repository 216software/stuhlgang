import store from './store';
import request from './request';

const login = ({ email, code }) => request('start-session-with-confirmation-code', {
  method: 'POST',
  body: JSON.stringify({
    email_address: email,
    confirmation_code: code,
  }),
});

const logout = () => request('logout', {
  method: 'POST',
  body: JSON.stringify({
    session_uuid: store.session(),
  }),
});

const verify = ({ session }) => {
  const params = new URLSearchParams(Object.entries({ session_uuid: session }));
  return request(`verify-session-uuid?${params}`);
};

const requestCode = ({ email }) => request('send-confirmation-code', {
  method: 'POST',
  body: JSON.stringify({
    email_address: email,
  }),
});

export {
  login,
  logout,
  verify,
  requestCode,
};
