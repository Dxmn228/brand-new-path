document.addEventListener('DOMContentLoaded', () => {
    const pop = document.querySelector('.registration_user');
    const user_window = document.querySelector('.user_window');
    if (pop && user_window) {pop.addEventListener('click', function() {
        user_window.classList.toggle('active');
    })};
});