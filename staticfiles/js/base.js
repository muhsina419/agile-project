document.addEventListener("DOMContentLoaded", function () {
    // Sidebar Navigation
    document.querySelectorAll("#sidebar ul li").forEach(item => {
        item.addEventListener("click", () => {
            const link = item.getAttribute("data-link");
            if (link) window.location.href = link;
        });
    });

    // User profile dropdown
    const userImage = document.getElementById("userImage");
    const userDetails = document.getElementById("userDetails");

    if (userImage && userDetails) {
        console.log("user..");
        
        userImage.addEventListener("click", (e) => {
            console.log("user2......");
            
            e.stopPropagation();
            userDetails.classList.toggle("hidden");
        });

        document.addEventListener("click", (e) => {
            if (!userDetails.contains(e.target) && e.target !== userImage) {
                console.log("user3....");
                
                userDetails.classList.add("hidden");
            }
        });
    }

    // Fetch profile photo dynamically
    const uniqueId = localStorage.getItem("id");
    if (uniqueId) {
        const profileImageUrl = `/media/images/${uniqueId}_profile.jpg`; // Adjust the path if necessary
        userImage.src = profileImageUrl;
    }

    

});

// Toggle Sidebar Menu
function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.style.transform = sidebar.style.transform === "translateX(-100%)"
            ? "translateX(0)"
            : "translateX(-100%)";
            sidebar.classList.remove("hidden")
    } else {
        console.error("Sidebar element not found");
    }
}

// Navigation Function
function navigate(page) {
    const body = document.body;
    const urls = {
        votersList: body.dataset.votersListUrl,
        candidatesList: body.dataset.candidatesListUrl,
        castVote: body.dataset.castVoteUrl,
        result: body.dataset.resultsUrl,
        editDetails: body.dataset.editDetailsUrl
    };

    if (urls[page]) {
        window.location.href = urls[page];
    } else {
        console.error("Navigation failed: Page not found -", page);
    }
}

// Logout Function
function logout() {
    const logoutUrl = document.body.dataset.logoutUrl;
    if (logoutUrl) {
        window.location.href = logoutUrl;
    } else {
        console.error("Logout URL not defined");
    }
}


