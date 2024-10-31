import axios from "axios";
import BASE_URL from "../base";

interface DoneExData {
  case_url: string;
  answer_to_id: number;
}

export const PostDoneEx = async (initData: string, data: DoneExData) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/cases/answer`,
      {
        case_url: data.case_url,
        answer_to_id: data.answer_to_id,
      },
      {
        headers: {
          "init-data": initData,
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error posting done exercise:", error);
    throw error;
  }
};
