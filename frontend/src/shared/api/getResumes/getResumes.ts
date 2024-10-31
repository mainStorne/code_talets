import axios from "axios";
import BASE_URL from "../base";

interface Resume {
  resume_url: string;
  user_id: number;
}

interface UserData {
  first_name: string;
  middle_name: string;
  phone_number: string;
  last_name: string;
  created_at: string;
  is_superuser: boolean;
  age: number;
  city: string;
  status: string;
  work_experience: string;
  id: number;
  resume: Resume;
}

export const getUserData = async (
  id: number,
  initData: string
): Promise<UserData> => {
  try {
    const response = await axios.get<UserData>(`${BASE_URL}/users/${id}`, {
      headers: {
        "Content-Type": "application/json",
        "init-data": initData,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Произошла ошибка при выполнении запроса:", error);
    throw error;
  }
};
