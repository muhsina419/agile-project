// Fetch voting statistics from the backend
async function fetchStats() {
  try {
    const response = await fetch("/api/vote-stats/");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch data:", error);
    return {
      totalVotes: 0,
      candidates: [],
      trend: [0, 0, 0, 0, 0, 0, 0], // Default trend data
    };
  }
}

// Submit a vote and refresh stats
async function castVote(candidateId) {
  try {
    const response = await fetch("/vote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidateId }),
    });
    if (!response.ok) {
      throw new Error("Failed to cast vote");
    }
    console.log("Vote cast successfully");
    await renderStats(); // Refresh stats after casting vote
  } catch (error) {
    console.error("Error casting vote:", error);
  }
}

// Render all statistics and the chart
async function renderStats() {
  const data = await fetchStats();
  const container = document.getElementById("stats-container");
  container.innerHTML = "";

  // Total Votes Card
  const totalVotesCard = createStatCard("Total Votes", data.totalVotes, "+0%");
  container.appendChild(totalVotesCard);

  // Candidate Cards
  data.candidates.forEach((candidate) => {
    const change = candidate.change || "+0%"; // Default change if not provided
    const card = createStatCard(`${candidate.name} Votes`, candidate.votes, change);
    card.addEventListener("click", () => castVote(candidate.id)); // Add click event to cast vote
    container.appendChild(card);
  });

  // Render the chart
  renderChart(data.trend);
}

// Initialize the stats rendering on page load
document.addEventListener("DOMContentLoaded", renderStats);