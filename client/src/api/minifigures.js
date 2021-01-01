import http from '../axios';

const pathname = '/minifigs';

export async function getMinifigures() {
  try {
    return await http.get(pathname);
  } catch (error) {
    throw new Error(error);
  }
}

export async function addMinifigure(data) {
  try {
    return await http.post(pathname, data);
  } catch (error) {
    throw new Error(error);
  }
}

export default getMinifigures;
