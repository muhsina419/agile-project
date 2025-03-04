document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".otp-input");

    inputs.forEach((input, index) => {
        input.addEventListener("input", (e) => {
            input.classList.remove("active");
            if (e.target.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].classList.add("active");
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && index > 0 && e.target.value === "") {
                inputs[index - 1].classList.add("active");
                inputs[index - 1].focus();
            }
        });
    });

    document.getElementById("verify-btn").addEventListener("click", () => {
        let otp = "";
        inputs.forEach(input => otp += input.value);
        if (otp.length === 6) {
            alert("OTP Verified: " + otp);
        } else {
            alert("Please enter a valid OTP.");
        }
    });
});
