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

export const uploadFile = async (file: File, initData: string) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${BASE_URL}/users/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "init-data": initData,
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export const postResumes = async (
  userData: UserData,
  file?: File,
  sendToAdmin: boolean = false
) => {
  const initData = window.Telegram.WebApp.initData;

  // Instead of requesting the phone number from Telegram, assume it's provided directly in userData

  try {
    const requestBody = {
      user: {
        first_name: userData.first_name || "string",
        middle_name: userData.middle_name || "string",
        last_name: userData.last_name || "string",
        created_at: new Date().toISOString(),
        is_superuser: false,
        age: userData.age || 13,
        city: userData.city || "string",
        work_experience: userData.work_experience || "string",
        phone_number: userData.phone_number,
      },
    };

    const response = await axios.post(
      `${BASE_URL}/users/register?send_to_admin=${sendToAdmin}`,
      requestBody,
      {
        headers: {
          "Content-Type": "application/json",
          "init-data": initData,
        },
      }
    );

    if (response.status === 200 && file) {
      await uploadFile(file, initData);
    }

    return response.data;
  } catch (error) {
    console.error("Error registering user:", error);
    throw error;
  }
};
