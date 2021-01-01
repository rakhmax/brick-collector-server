import http from '../axios';

async function searchData(query) {
  try {
    const { data } = await http.get(`search?query=${query}`);
    return data || [];
  } catch (error) {
    return error;
  }
}

export default searchData;
