// Profile.tsx
import { useQuery } from "@tanstack/react-query";
import { getRequests } from "../shared/api/requests";

const Profile = () => {
  const { data, error, isLoading } = useQuery({
    queryKey: ["profileData"],
    queryFn: getRequests,
  });

  if (isLoading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>Ошибка: {error.message}</div>;
  }

  return (
    <div>
      <h1>Профиль</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>{" "}
    </div>
  );
};

export default Profile;
