//import image from '../assets/logo.jpg';
import TravelAppLogo from '../assets/logo.jpg'
import './Logo.css'
//logo component
const Logo = () => {
  return (
    <img src={TravelAppLogo} alt="Logo" className="logo" />
  );
}

export default Logo;