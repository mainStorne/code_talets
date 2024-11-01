import axios from "axios";
import BASE_URL from "../base";

interface User {
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
}

interface UserResume {
  id: number;
  resume_url: string;
  user_id: number;
}

interface Case {
  case_url: string;
  executor_id: number;
  creator_id: number;
  exp_at: string;
  id: number;
}

interface CaseAnswer {
  case_url: string;
  answer_to_id: number;
  created_at: string;
  id: number;
}

export const getFull = async (
  id: number,
  initData: string
): Promise<{
  user: User;
  user_resume: UserResume;
  case: Case;
  case_answer: CaseAnswer;
}> => {
  try {
    const response = await axios.get<{
      user: User;
      user_resume: UserResume;
      case: Case;
      case_answer: CaseAnswer;
    }>(`${BASE_URL}/answer_cases/user_case/${id}`, {
      headers: {
        "init-data": initData,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};
