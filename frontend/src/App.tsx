import { useState } from 'react'
import './App.css'
import { getContributor } from './apiClient'
import type { ContributorReadWithAchievements } from './apiClient';

function App() {
  const [username, setUsername] = useState('torvalds') // Default user for demo
  const [contributor, setContributor] = useState<ContributorReadWithAchievements | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSearch = () => {
    if (!username) return;
    setLoading(true);
    setError('');
    setContributor(null);

    getContributor(username)
      .then(data => {
        setContributor(data);
      })
      .catch(err => {
        setError(`Failed to find contributor: ${err.message}`);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  return (
    <>
      <h1>OSPO-ColabAchievements</h1>
      <div className="card">
        <div style={{ display: 'flex', gap: '8px' }}>
          <input 
            type="text" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter GitHub username"
          />
          <button onClick={handleSearch} disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {contributor && (
        <div className="card">
          <h2>{contributor.github_username}</h2>
          <img src={contributor.avatar_url} alt={`${contributor.github_username}'s avatar`} width={100} />
          <h3>Achievements:</h3>
          {contributor.achievements.length > 0 ? (
            <ul>
              {contributor.achievements.map(ach => (
                <li key={ach.id}>{ach.title}: {ach.description}</li>
              ))}
            </ul>
          ) : (
            <p>No achievements yet.</p>
          )}
        </div>
      )}
    </>
  )
}

export default App
