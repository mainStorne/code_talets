import axios from "axios";
import BASE_URL from "../../../shared/api/base";

interface CaseData {
  case_url: string;
  text: string;
  creator_id: number;
  executor_id: number;
  start_time: string;
  exp_at: string;
}

export const postCase = async (initData: string, caseData: CaseData) => {
  try {
    const response = await axios.post(`${BASE_URL}/cases`, caseData, {
      headers: {
        "Content-Type": "application/json",
        "init-data": initData,
        "ngrok-skip-browser-warning": "69420",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error posting case:", error);
    throw error;
  }
};
