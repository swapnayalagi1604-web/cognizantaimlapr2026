//create api to show flight information
const express = require('express');
const app = express();
//add cors and body-parser
const cors = require('cors');
const bodyParser = require('body-parser');
app.use(cors());
app.use(bodyParser.json());
const port = 3000;

app.get('/flights', (req, res) => {
  // Sample flight data
  const flights = [
    { id: 1, airline: 'Airline A', departure: 'City A', arrival: 'City B' },
    { id: 2, airline: 'Airline B', departure: 'City C', arrival: 'City D' },
  ];
  res.json(flights);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
