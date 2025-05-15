const sidebar = document.getElementById('sidebar');
    const menu = document.getElementById('menu-icon');       
        menu.addEventListener("click", () => { 
              sidebar.classList.toggle("hidden");
          });

document.addEventListener("DOMContentLoaded", function () {
    // Sidebar Navigation
    document.querySelectorAll(".sidebar li").forEach(item => {
        item.addEventListener("click", () => {
            const link = item.getAttribute("data-link");
            if (link) window.location.href = link;
        });
    });

    // User profile dropdown
    const userImage = document.getElementById("userImage");
    const userDetails = document.getElementById("userDetails");

    if (userImage && userDetails) {
        userImage.addEventListener("click", (e) => {
            e.stopPropagation();
            userDetails.classList.toggle("hidden");
        });

        document.addEventListener("click", (e) => {
            if (!userDetails.contains(e.target) && e.target !== userImage) {
                userDetails.classList.add("hidden");
            }
        });
    }
});
