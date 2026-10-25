const pop = document.querySelector('.registration_user');
const user_window = document.querySelector('.user_window');

function open_user_window() {
    if (pop) {
        user_window.classList.toggle('active');
    }
}

function close_user_window() {
    if (user_window) {
        user_window.classList.remove('active');
    }
}
