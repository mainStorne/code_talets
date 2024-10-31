import axios from "axios";
import BASE_URL from "../base";

export const sendAnswers = async (answers: number[], initData: string) => {
  try {
    const response = await axios.post(`${BASE_URL}/quote/`, answers, {
      headers: {
        "Content-Type": "application/json",
        "init-data": initData,
      },
    });

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка при регистрации пользователя:", error);
    throw error;
  }
};
