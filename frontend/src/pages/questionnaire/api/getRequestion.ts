import axios from "axios";
import BASE_URL from "../../../shared/api/base";

export interface QuestionData {
  items?: Array<{
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
  size: number = 4, // Default size to 4
  initData: string // Pass initData as an argument
): Promise<QuestionData> => {
  try {
    const response = await axios.get(`${BASE_URL}/quote/`, {
      params: {
        page, // shorthand for page: page
        size, // shorthand for size: size
      },
      headers: {
        "init-data": initData,
        "ngrok-skip-browser-warning": "69420", // Use initData from the Telegram WebApp
      },
    });

    console.log("Response data:", response.data);
    return response.data; // Return the response data
  } catch (error) {
    console.error("Error fetching questions:", error);
    throw error; // Rethrow the error for handling further up the call stack
  }
};
