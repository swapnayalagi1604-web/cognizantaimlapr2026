import Logo from './Logo/Logo';
import Timer from './Timer/Timer';
import Flight from './Flights/Flight';
import './App.css';
function App() {


  return (
    <section>
    <section className="app">
      <Logo />
      <h1>Travel App</h1>
      <Timer className="timer" />
    </section>
    <section>
      <Flight></Flight>
    </section>
    </section>
  )
}

export default App
