const setItem = (key, value) => new Promise((resolve, reject) => {
  NativeStorage.setItem(key, value, (result) => {
    resolve(result);
  }, (error) => {
    reject(error);
  });
});

const getItem = key => new Promise((resolve, reject) => {
  NativeStorage.getItem(key, (result) => {
    resolve(result);
  }, (error) => {
    reject(error);
  });
});

const removeItem = key => new Promise((resolve, reject) => {
  NativeStorage.remove(key, () => {
    resolve();
  }, (error) => {
    reject(error);
  });
});

export {
  setItem,
  getItem,
  removeItem,
};
