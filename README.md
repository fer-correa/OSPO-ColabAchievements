# OSPO-ColabAchievements

OSPO-ColabAchievements is a web application designed to track, recognize, and showcase contributions to open source and inner source projects, going beyond just code contributions. It aims to provide publishable achievements for developers and other contributors, fostering community engagement and learning.

## Architecture

The project follows a modern web application architecture:

-   **Backend**: Developed with Python using the FastAPI framework, SQLModel (ORM), and SQLite (database).
-   **Worker**: A separate Python script responsible for fetching contribution data from platforms like GitHub and populating the database via the Backend API.
-   **Frontend**: Built with React and Vite, providing an interactive user interface.

## Features

-   Track contributions (Pull Requests, Issues, Commits) from GitHub repositories.
-   Support for processing contributions from specific repositories or entire GitHub organizations.
-   API-driven data pipeline for flexible data access.
-   (Future) AI-powered summarization and title generation for achievements.
-   (Future) Recognition of non-code contributions.

## Setup and Running the Project

To get the OSPO-ColabAchievements application running locally, follow these steps:

### Prerequisites

-   Python 3.9+ and `pip`
-   Node.js 18+ and `npm`
-   A GitHub Personal Access Token (PAT) with `public_repo` scope (needed for the worker to fetch data).

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd OSPO-ColabAchievements
```

### 2. Backend Setup and Run

Open your first terminal and navigate to the project root:

```bash
cd OSPO-ColabAchievements
```

Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the FastAPI backend server:

```bash
uvicorn backend.main:app --reload
```

This will start the API server on `http://127.0.0.1:8000`.

### 3. Frontend Setup and Run

Open your second terminal and navigate to the frontend directory:

```bash
cd OSPO-ColabAchievements/frontend
```

Install Node.js dependencies:

```bash
npm install
```

Run the React development server:

```bash
npm run dev
```

This will start the frontend and provide a URL, usually `http://localhost:5173`.

### 4. Worker Configuration and Run

Open your third terminal and navigate to the project root:

```bash
cd OSPO-ColabAchievements
```

Configure the worker by editing `ospo_config.yml`:

```yaml
# ospo_config.yml

# List of GitHub organizations to scan for contributions.
organizations:
  - "todogroup" # Example: will fetch repos from TODOGroup

# Or, a specific list of repositories
repositories:
  # - "owner/repo1"
  # - "owner/repo2"
```

Set your GitHub Personal Access Token as an environment variable:

```bash
export GH_TOKEN="your_github_pat_here"
```

Run the worker script to populate the database:

```bash
python -m backend.worker
```

### 5. View the Application

Open your web browser and go to the frontend URL (e.g., `http://localhost:5173`). You can then use the search bar to find contributors whose data has been processed by the worker.

## Development

### Running Tests

(Future: Instructions for running backend and frontend tests will go here.)

## Contributing

(Future: Guidelines for contributing to the project will go here.)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
