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

export const fetchQuestions = async (page: number, size: number, initData: string): Promise<QuestionData> => {
  try {
    const response = await axios.get(`${BASE_URL}/quote/`, {
			params: {
				page: page,
				size: size
			},
      headers: {
				"init-data": initData,
      },
    });
		console.log("response data:"+response.data)
    return response.data;
  } catch (error) {
    console.error("Ошибка при получении вопросов:", error);
    throw error;
  }
};
