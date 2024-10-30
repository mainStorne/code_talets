import { NavLink } from "react-router-dom";
import { CONTENT_NAVIGATION_MENU } from "../../../shared/consts/contentNavMenu";

export const Header = () => {
  const navigationContent = CONTENT_NAVIGATION_MENU.map((item) => (
    <li key={item.title}>
      <NavLink to={item.link}>{item.title}</NavLink>
    </li>
  ));

  return <ul className="header__navigation-menu-list">{navigationContent}</ul>;
};

export default Header;
