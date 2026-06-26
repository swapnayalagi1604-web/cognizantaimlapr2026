import { useState,useEffect} from 'react';

function Flight() {
   //flights state
   const [flights, setFlights] = useState([]);

   useEffect(() => {
    // Fetch flight data from the backend API
    fetch('http://localhost:3000/flights')
        .then(response => response.json())
        .then(data => setFlights(data))
        .catch(error => console.error('Error fetching flight data:', error));
}, []);


    return (
        <div className="flight">
            <h2>Flight Information</h2>
            <ul>
                {flights.map(flight => (
                    <li key={flight.id}>
                        {flight.airline} - {flight.arrival} to {flight.departure} at {flight.time}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Flight;