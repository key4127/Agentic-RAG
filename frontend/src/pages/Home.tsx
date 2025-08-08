import { UserInput } from "../components/commons/Input";
import { HomeHeader } from "../components/headers/HomeHeader";

export function Home() {
  return (
    <div>
      <HomeHeader />
      <br />
      <UserInput />
    </div>
  )
}