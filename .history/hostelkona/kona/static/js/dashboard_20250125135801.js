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

// Select the checkbox and the body
const switchModeCheckbox = document.getElementById('switch-mode');
const body = document.body;

// Check if the checkbox is already checked (for page load)
if (switchModeCheckbox.checked) {
  body.classList.add('dark-theme');
} else {
  body.classList.add('light-theme');
}

// Add an event listener to toggle the theme when the checkbox changes
switchModeCheckbox.addEventListener('change', () => {
  if (switchModeCheckbox.checked) {
    body.classList.add('dark-theme');
    body.classList.remove('light-theme');
  } else {
    body.classList.add('light-theme');
    body.classList.remove('dark-theme');
  }
});

