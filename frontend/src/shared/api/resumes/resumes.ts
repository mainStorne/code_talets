import axios from "axios";
import BASE_URL from "../base";

export interface UserData {
  first_name?: string;
  middle_name?: string;
  last_name?: string;
  age?: number;
  city?: string;
  work_experience?: string;
  phone_number?: string;
}

export const postResumes = async (
  userData: UserData,
  file?: File,
  sendToAdmin: boolean = true
) => {
  const initData = window.Telegram.WebApp.initData;

  try {
    const formData = new FormData();
    formData.append(
      "user",
      new Blob(
        [
          JSON.stringify({
            first_name: userData.first_name || "string",
            middle_name: userData.middle_name || "string",
            last_name: userData.last_name || "string",
            created_at: new Date().toISOString(),
            is_superuser: false,
            age: userData.age || 18,
            city: userData.city || "string",
            work_experience: userData.work_experience || "string",
            phone_number: userData.phone_number,
          }),
        ],
        { type: "application/json" }
      )
    );

    if (file) {
      formData.append("file", file);
    }

    const response = await axios.post(
      `${BASE_URL}/users/register?send_to_admin=${sendToAdmin}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          "init-data": initData,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error registering user:", error);
    throw error;
  }
};
