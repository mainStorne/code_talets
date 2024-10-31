import axios from "axios";
import BASE_URL from "../base";

export interface QuestionData {
  items: Array<{
    name: string;
    speciality_id: number;
    id: number;
  }>;
  total?: number;
  page?: number;
  size?: number;
  pages?: number;
}

export const fetchQuestions = async (
  page: number,
  size: number = 4,
  initData: string
): Promise<QuestionData> => {
  try {
    const response = await axios.get(`${BASE_URL}/quote/`, {
      params: {
        page,
        size,
      },
      headers: {
        "init-data": initData,
        "ngrok-skip-browser-warning": "69420",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching questions:", error);
    throw error;
  }
};
