const request = async (location, options = {}) => {
  const url = `${API_URL}/${location}`;

  try {
    const response = await fetch(url, options);
    const json = await response.json();
    return json;
  } catch (error) {
    throw error;
  }
};

export default request;
