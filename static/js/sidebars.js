document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.querySelector('.menu-toggle');

    // Fungsi untuk membuka/tutup sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('active');
    }

    // Event listener untuk tombol hamburger
    menuToggle.addEventListener('click', toggleSidebar);
});
