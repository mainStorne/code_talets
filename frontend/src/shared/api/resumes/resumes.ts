import axios from "axios";
import BASE_URL from "../base";

export interface UserData {
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  age?: number;
  city?: string;
  work_experience?: string;
}

export const postResumes = async (userData: UserData) => {
  // Получаем init_data из Telegram WebApp
  const initData = window.Telegram.WebApp.initData;

  const requestBody = {
    user: {
      first_name: userData.first_name || "string",
      middle_name: userData.middle_name || "string",
      last_name: userData.last_name || "string",
      created_at: new Date().toISOString(),
      is_superuser: false,
      age: userData.age || 13,
      city: userData.city || "string",
      work_experience: userData.work_experience || "string",
    },
    init_data: initData,
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
