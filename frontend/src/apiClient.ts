export type Achievement = {
    id: number;
    title: string;
    description: string;
    awarded_at: string; // Dates will be strings over JSON
    source_contribution_url?: string;
}

export type ContributorReadWithAchievements = {
    id: number;
    github_username: string;
    avatar_url: string;
    achievements: Achievement[];
}

const API_BASE_URL = 'http://127.0.0.1:8000';

export async function getContributor(username: string): Promise<ContributorReadWithAchievements> {
    const response = await fetch(`${API_BASE_URL}/contributors/${username}/`);
    if (!response.ok) {
        throw new Error(`Failed to fetch contributor: ${response.statusText}`);
    }
    return response.json();
}
