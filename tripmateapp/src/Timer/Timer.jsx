import { useState,useEffect } from 'react';
import './Timer.css';
function Timer() {
  
    //initializing the state variable
    const[currentTime, setCurrentTime] = useState(new Date());
    //function to update the time
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);   
        return () => clearInterval(timer);

}, []);

return (
    <div className="timer">
        <h4 >{currentTime.toLocaleTimeString()}</h4>
    </div>
);

}

export default Timer;