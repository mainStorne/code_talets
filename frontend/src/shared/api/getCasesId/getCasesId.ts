import axios from "axios";
import BASE_URL from "../base";

interface CaseData {
  case_url: string;
  text: string;
  executor_id: number;
  creator_id: number;
  exp_at: string;
  id: number;
}

type GetCaseDataParams = {
  id: number;
  initData: string;
};

export const GetCaseData = async ({
  id,
  initData,
}: GetCaseDataParams): Promise<CaseData> => {
  try {
    const response = await axios.get<CaseData>(`${BASE_URL}/cases/${id}`, {
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
