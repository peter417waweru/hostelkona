document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menu-icon');
    const sidebar = document.getElementById('sidebar');
    const closeBtn = document.getElementById('close-btn');

    // Open sidebar when menu icon is clicked
    menuIcon.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // Close sidebar when close button is clicked
    closeBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        sidebar.classList.remove('active');
    });
});
