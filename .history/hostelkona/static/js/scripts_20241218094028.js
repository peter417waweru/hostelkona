// Select elements
const menuIcon = document.getElementById("menu-icon");
const sidebar = document.getElementById("sidebar");
const closeBtn = document.getElementById("close-btn");

// Show the sidebar when the menu icon is clicked
menuIcon.addEventListener("click", () => {
    sidebar.classList.add("active"); // Add 'active' class to display sidebar
});

// Hide the sidebar when the close button is clicked
closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("active"); // Remove 'active' class to hide sidebar
});
