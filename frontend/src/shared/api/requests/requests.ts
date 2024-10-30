import BASE_URL from "../base";

export const getRequests = async () => {
  const response = await fetch(`${BASE_URL}/points`);
  if (!response.ok) {
    throw new Error("Ошибка при получении данных");
  }
  const data = await response.json();
  return data;
};
