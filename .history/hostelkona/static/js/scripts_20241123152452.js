document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const menuButton = document.querySelector(".menu-button");
    const closeButton = document.querySelector(".sidebar li a:first-child");

    // Function to show the sidebar
    const showSidebar = () => {
        sidebar.style.display = "flex";
        sidebar.classList.add("active");
    };

    // Function to hide the sidebar
    const hideSidebar = () => {
        sidebar.style.display = "none";
        sidebar.classList.remove("active");
    };

    // Event listeners for opening and closing the sidebar
    menuButton.addEventListener("click", (e) => {
        e.preventDefault();
        showSidebar();
    });

    closeButton.addEventListener("click", (e) => {
        e.preventDefault();
        hideSidebar();
    });

    // Close the sidebar when clicking outside of it
    document.addEventListener("click", (e) => {
        if (!sidebar.contains(e.target) && !menuButton.contains(e.target)) {
            hideSidebar();
        }
    });

    // Ensure the sidebar is hidden on larger screens
    window.addEventListener("resize", () => {
        if (window.innerWidth > 800) {
            sidebar.style.display = "none";
        }
    });
});
