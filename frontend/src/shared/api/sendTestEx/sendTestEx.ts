import axios from "axios";
import BASE_URL from "../../../shared/api/base";

interface CaseData {
  case_url: string;
  text: string;
  creator_id: number;
  executor_id: number;
  exp_at: string;
}

export const postCase = async (initData: string, caseData: CaseData) => {
  try {
    // Create FormData instance
    const formData = new FormData();

    // Append the `caseData` object as JSON
    formData.append(
      "objs",

      JSON.stringify({
        creator_id: caseData.creator_id,
        case_url: caseData.case_url,
        text: caseData.text,
        executor_id: caseData.executor_id,
        exp_at: caseData.exp_at,
      })
    );

    // Make the POST request
    const response = await axios.post(`${BASE_URL}/cases/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data", // This can also be omitted as axios will set it automatically
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
