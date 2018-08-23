const setItem = (key, value) => new Promise((resolve) => {
  NativeStorage.setItem(key, value, (result) => {
    resolve(result);
  }, (error) => {
    throw error;
  });
});

const getItem = key => new Promise((resolve) => {
  NativeStorage.getItem(key, (result) => {
    resolve(result);
  }, (error) => {
    throw error;
  });
});

const removeItem = key => new Promise((resolve) => {
  NativeStorage.remove(key, () => {
    resolve();
  }, (error) => {
    throw error;
  });
});

export {
  setItem,
  getItem,
  removeItem,
};
