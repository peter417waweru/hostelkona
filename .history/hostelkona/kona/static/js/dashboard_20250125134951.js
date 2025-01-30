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


// Select the sidebar and the toggle button
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');

// Add click event listener to the toggle button
sidebarToggle.addEventListener('click', () => {
  // Toggle the 'hide' class on the sidebar
  sidebar.classList.toggle('hide');
});

const body = document.body;
const themeToggleButton = document.getElementById('theme-toggle-button'); // Assuming you have a button for theme switching

themeToggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-theme');
    body.classList.toggle('light-theme');
});

