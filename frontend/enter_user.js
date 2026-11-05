const pop = document.querySelector('.enter_user');
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

const loginForm = document.querySelector("#login-form");
const loginMessage = document.querySelector("#login-message");

if (loginForm && loginMessage) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const emailOrPhone =
            loginForm.elements.identifier.value.trim();

        const password =
            loginForm.elements.password.value;

        loginMessage.textContent = "Выполняется вход...";

        const submitButton = loginForm.querySelector(
            'button[type="submit"]'
        );

        submitButton.disabled = true;

        try {
            const data = await loginUser(emailOrPhone, password);

            // Сохраняем access-токен на время текущей вкладки.
            sessionStorage.setItem(
                "access_token",
                data.access_token
            );

            loginMessage.textContent = "Вход выполнен успешно!";

            console.log("Авторизация успешна");

            // Здесь позже можно закрыть окно входа
            // и показать профиль пользователя.

        } catch (error) {
            loginMessage.textContent =
                error.message || "Не удалось выполнить вход";

        } finally {
            submitButton.disabled = false;
        }
    });
}
