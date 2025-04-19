async function loadVoters() {
    const response = await fetch('/api/voters-list/');
    const voters = await response.json();

    const tbody = document.getElementById('voterTable');
    tbody.innerHTML = '';

    voters.forEach(voter => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <img class="voter-photo" src="${voter.photo}" alt="Photo"
                     onclick='showVoterDetails(${JSON.stringify(voter)})'
                     onerror="this.src='/static/images/default-photo.png'">
            </td>
            <td><div class="voter-id">${voter.unique_id}</div></td>
            <td><div class="voter-name">${voter.name}</div></td>
        `;
        tbody.appendChild(row);
    });
}
// Show voter details in the modal
function showVoterDetails(voter) {
    const voterDetails = document.getElementById('voterDetails');
    voterDetails.innerHTML = `
      <div class="voter-card">
        <button class="close-btn" onclick="closeVoterDetails()">×</button>
        <img src="${voter.photo || '/static/images/default-photo.png'}" alt="Voter Photo">
        <p><strong>Name:</strong> ${voter.name}</p>
        <p><strong>Unique ID:</strong> ${voter.unique_id}</p>
        <p><strong>Email:</strong> ${voter.email || 'N/A'}</p>
        <p><strong>Phone:</strong> ${voter.phone || 'N/A'}</p>
        <p><strong>Voting Status:</strong> ${voter.voting_status ? 'Voted' : 'Pending'}</p>
      </div>
    `;
    voterDetails.classList.remove('hidden');
}
  
  // Close voter details modal
function closeVoterDetails() {
    const voterDetails = document.getElementById('voterDetails');
    voterDetails.classList.add('hidden');
}

// Filter voters by search input
function filterVoters() {
    const searchInput = document.querySelector('.search-input').value.toLowerCase();
    const voterRows = document.querySelectorAll('.voter-row:not(.header)');
    voterRows.forEach(row => {
      const voterName = row.querySelector('.voter-name').textContent.toLowerCase();
      const voterId = row.querySelector('.voter-id').textContent.toLowerCase();
      row.style.display = voterName.includes(searchInput) || voterId.includes(searchInput) ? '' : 'none';
    });
  }

window.onload = loadVoters;
