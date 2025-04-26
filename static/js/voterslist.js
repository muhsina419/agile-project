// Remove or comment out the dynamic table rendering code
// const votersListContainer = document.querySelector('.voters-list-container');
// votersListContainer.innerHTML = `
//   <div class="voter-row header">
//       <span>Photo</span>
//       <span>Unique ID</span>
//       <span>Name</span>
//   </div>
// `;

// voters.forEach(voter => {
//   const voterRow = document.createElement('div');
//   voterRow.classList.add('voter-row');
//   voterRow.setAttribute('onclick', `showVoterDetails(${JSON.stringify(voter)})`);
//   voterRow.innerHTML = `
//     <div class="voter-photo">
//       <img src="${voter.photo || '/static/images/default-photo.png'}" alt="Voter Photo" onerror="this.src='/static/images/default-photo.png'">
//     </div>
//     <div class="voter-id">${voter.unique_id}</div>
//     <div class="voter-name">${voter.full_name}</div>
//   `;
//   votersListContainer.appendChild(voterRow);
// });

// Keep only the search functionality
function filterVoters() {
  const searchInput = document.querySelector('.search-box').value.toLowerCase();
  const voterRows = document.querySelectorAll('.table-row:not(.header)');

  voterRows.forEach(row => {
    const voterName = row.querySelector('.name').textContent.toLowerCase();
    const voterId = row.querySelector('.uid').textContent.toLowerCase();

    if (voterName.includes(searchInput) || voterId.includes(searchInput)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Attach the search functionality
document.querySelector('.search-box').addEventListener('keyup', filterVoters);