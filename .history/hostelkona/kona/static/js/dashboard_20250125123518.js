document.addEventListener("DOMContentLoaded", () => {
    const switchMode = document.getElementById("switch-mode");

    // Check for saved theme in localStorage
    const currentTheme = localStorage.getItem("theme");
    if (currentTheme === "dark") {
        document.body.classList.add("dark");
        switchMode.checked = true;
    }

    // Toggle theme when the checkbox is clicked
    switchMode.addEventListener("change", () => {
        if (switchMode.checked) {
            document.body.classList.add("dark");
            localStorage.setItem("theme", "dark");
        } else {
            document.body.classList.remove("dark");
            localStorage.setItem("theme", "light");
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebar-toggle");

    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.toggle("hidden");
    });
});
