import axios from "axios";
import BASE_URL from "../base";

interface UpdateUserData {
  first_name?: string;
  middle_name?: string;
  phone_number?: string;
  last_name?: string;
  created_at?: string;
  is_superuser?: boolean;
  age?: number;
  city?: string;
  status?: string;
  work_experience?: string;
}

export const patchUser = async (
  id: number,
  data: UpdateUserData,
  initData: string
): Promise<void> => {
  try {
    await axios.patch(`${BASE_URL}/users/${id}`, data, {
      headers: {
        "init-data": initData,
      },
    });
  } catch (error) {
    console.error("Error updating user data:", error);
    throw error;
  }
};
