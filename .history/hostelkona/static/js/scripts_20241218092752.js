// Get elements
const menuIcon = document.getElementById("menu-icon");
const sidebar = document.getElementById("sidebar");
const closeBtn = document.getElementById("close-btn");

// Open sidebar
menuIcon.addEventListener("click", () => {
    sidebar.classList.add("active");
});

// Close sidebar
closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("active");
});

// Close sidebar when clicking a link
const sidebarLinks = sidebar.querySelectorAll("a");
sidebarLinks.forEach(link => {
    link.addEventListener("click", () => {
        sidebar.classList.remove("active");
    });
});
