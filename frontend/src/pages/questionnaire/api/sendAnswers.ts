import axios from "axios";
import BASE_URL from "../../../shared/api/base";

export interface TestData {
  data: number[]; // Массив с ответами, где каждый ответ представлен числом
}

export const sendAnswers = async (testData: TestData) => {
  // Получаем init_data из Telegram WebApp
  const initData = window.Telegram.WebApp.initData;

  // Преобразуем массив данных в объект с номерами вопросов в качестве ключей
  const answers = testData.data.reduce((acc, answer, index) => {
    acc[(index + 1).toString()] = answer; // Ключи: '1', '2', и так далее
    return acc;
  }, {} as Record<string, number>);

  const requestBody = {
    answers,
    init_data: initData, // Добавляем initData
  };

  try {
    const response = await axios.post(
      `${BASE_URL}/api/users/register`,
      requestBody,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Ошибка при регистрации пользователя:", error);
    throw error;
  }
};
