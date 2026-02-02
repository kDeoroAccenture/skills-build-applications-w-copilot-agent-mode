import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import octofitLogo from './octofitapp-small.png';

function App() {
	return (
		<>
			<nav className="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
				<div className="container">
					<Link className="navbar-brand fw-bold d-flex align-items-center" to="/">
						<img src={octofitLogo} alt="OctoFit Logo" className="octofit-logo me-2" />
						OctoFit Tracker
					</Link>
					<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse" id="navbarNav">
						<ul className="navbar-nav ms-auto">
							<li className="nav-item"><Link className="nav-link" to="/activities">Activities</Link></li>
							<li className="nav-item"><Link className="nav-link" to="/leaderboard">Leaderboard</Link></li>
							<li className="nav-item"><Link className="nav-link" to="/teams">Teams</Link></li>
							<li className="nav-item"><Link className="nav-link" to="/users">Users</Link></li>
							<li className="nav-item"><Link className="nav-link" to="/workouts">Workouts</Link></li>
						</ul>
					</div>
				</div>
			</nav>
			<div className="container">
				<Routes>
					<Route path="/activities" element={<Activities />} />
					<Route path="/leaderboard" element={<Leaderboard />} />
					<Route path="/teams" element={<Teams />} />
					<Route path="/users" element={<Users />} />
					<Route path="/workouts" element={<Workouts />} />
					<Route path="/" element={
						<div className="text-center mt-5">
							<div className="card shadow p-4">
								<h1 className="display-4 mb-3">Welcome to <span className="text-primary">OctoFit Tracker</span>!</h1>
								<p className="lead">Track your fitness, join teams, and compete on the leaderboard.</p>
								<Link to="/activities" className="btn btn-primary btn-lg mt-3">Get Started</Link>
							</div>
						</div>
					} />
				</Routes>
			</div>
		</>
	);
}

export default App;
