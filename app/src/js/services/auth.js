import store from './store';
import request from './request';

const login = ({ email, password }) => request('login', {
  method: 'POST',
  body: JSON.stringify({
    email_address: email,
    password,
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

export {
  login,
  logout,
  verify,
};
