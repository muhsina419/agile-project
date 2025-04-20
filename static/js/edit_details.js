document.getElementById('updateForm').addEventListener('submit', async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const formData = {
      fullName: form.fullName.value,
      email: form.email.value,
      phone: form.phone.value,
      dob: form.dob.value,
      address: form.address.value,
    };
  
    const messageElement = document.getElementById('responseMessage');
    messageElement.textContent = "Updating...";
  
    try {
      const response = await fetch('/api/update-profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add CSRF token here if using Django templates
        },
        body: JSON.stringify(formData),
      });
  
      if (response.ok) {
        messageElement.textContent = "Updated successfully!";
        messageElement.style.color = 'green';
      } else {
        messageElement.textContent = "Error updating. Please try again.";
        messageElement.style.color = 'red';
      }
    } catch (error) {
      console.error(error);
      messageElement.textContent = "Network error. Try again.";
      messageElement.style.color = 'red';
    }
  });
  
  document.getElementById('resetForm').addEventListener('click', function () {
    document.getElementById('updateForm').reset();
    document.getElementById('responseMessage').textContent = "";
  });
  