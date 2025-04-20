async function loadVoters() {
  const response = await fetch('/api/voters-list/');
  const voters = await response.json();

  const votersListContainer = document.querySelector('.voters-list-container');
  votersListContainer.innerHTML = `
    <div class="voter-row header">
        <span>Photo</span>
        <span>Unique ID</span>
        <span>Name</span>
    </div>
  `;

  voters.forEach(voter => {
    const voterRow = document.createElement('div');
    voterRow.classList.add('voter-row');
    voterRow.setAttribute('onclick', `showVoterDetails(${JSON.stringify(voter)})`);
    voterRow.innerHTML = `
      <div class="voter-photo">
        <img src="${voter.photo || '/static/images/default-photo.png'}" alt="Voter Photo" onerror="this.src='/static/images/default-photo.png'">
      </div>
      <div class="voter-id">${voter.unique_id}</div>
      <div class="voter-name">${voter.full_name}</div>
    `;
    votersListContainer.appendChild(voterRow);
  });

  // Set up the search event listener after loading voters
  const searchInput = document.querySelector('.search-input');
  searchInput.addEventListener('keyup', filterVoters);
}

// Show voter details in a modal
function showVoterDetails(voter) {
  const voterDetails = document.getElementById('voterDetails');
  voterDetails.innerHTML = `
    <div class="voter-card">
      <button class="close-btn" onclick="closeVoterDetails()">×</button>
      <img src="${voter.photo || '/static/images/default-photo.png'}" alt="Voter Photo">
      <p><strong>Name:</strong> ${voter.full_name}</p>
      <p><strong>Unique ID:</strong> ${voter.unique_id}</p>
      <p><strong>Email:</strong> ${voter.email || 'N/A'}</p>
      <p><strong>Phone:</strong> ${voter.phone || 'N/A'}</p>
      <p><strong>Voting Status:</strong> ${voter.voting_status ? 'Voted' : 'Pending'}</p>
    </div>
  `;
  voterDetails.classList.remove('hidden');
}

// Close the voter details modal
function closeVoterDetails() {
  document.getElementById('voterDetails').classList.add('hidden');
}

// Filter voter rows based on input
function filterVoters() {
  const searchInput = document.querySelector('.search-input').value.toLowerCase();
  const voterRows = document.querySelectorAll('.voter-row:not(.header)');

  voterRows.forEach(row => {
    const voterName = row.querySelector('.voter-name').textContent.toLowerCase();
    const voterId = row.querySelector('.voter-id').textContent.toLowerCase();

    if (voterName.includes(searchInput) || voterId.includes(searchInput)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Call loadVoters on page load
window.onload = loadVoters;
