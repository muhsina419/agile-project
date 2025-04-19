document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("candidateTableBody");
    const form = document.getElementById("votingForm");
    const clearBtn = document.getElementById("clearBtn");
  
    // Fetch candidates from backend
    fetch("/api/candidates")
      .then(response => response.json())
      .then(candidates => {
        tableBody.innerHTML = "";
  
        candidates.forEach((candidate, index) => {
          const row = document.createElement("tr");
  
          row.innerHTML = `
            <td>${index + 1}</td>
            <td>${candidate.name}</td>
            <td><img src="${candidate.photo}" class="avatar" alt="Photo" /></td>
            <td><img src="${candidate.symbol}" class="symbol-img" alt="Symbol" /></td>
            <td><input type="checkbox" name="vote" value="${candidate._id}" class="vote-checkbox" /></td>
          `;
  
          tableBody.appendChild(row);
        });
  
        // Allow only one checkbox at a time
        setupSingleSelection();
      })
      .catch(err => {
        console.error("Failed to load candidates:", err);
        tableBody.innerHTML = `<tr><td colspan="5">Error loading candidates.</td></tr>`;
      });
  
    function setupSingleSelection() {
      const checkboxes = document.querySelectorAll(".vote-checkbox");
  
      checkboxes.forEach(box => {
        box.addEventListener("change", () => {
          if (box.checked) {
            checkboxes.forEach(cb => {
              if (cb !== box) cb.checked = false;
            });
          }
        });
      });
  
      clearBtn.addEventListener("click", () => {
        checkboxes.forEach(cb => cb.checked = false);
      });
  
      form.addEventListener("submit", e => {
        e.preventDefault();
        const selected = [...checkboxes].find(cb => cb.checked);
  
        if (!selected) {
          alert("Please select a candidate before submitting.");
          return;
        }
  
        const voteData = { candidateId: selected.value };
  
        fetch("/api/vote", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(voteData)
        })
          .then(res => {
            if (!res.ok) throw new Error("Vote submission failed");
            return res.json();
          })
          .then(data => {
            console.log("Vote submitted successfully:", data);
            window.location.href = "/voting_success/";
          })
          .catch(err => {
            console.error("Error submitting vote:", err);
            alert("Failed to submit vote. Please try again.");
          });
      });
    }
  });
  