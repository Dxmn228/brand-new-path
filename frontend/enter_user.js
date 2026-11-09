const user_window = document.querySelector('.user_window');
const authControls = document.querySelector('#auth_controls');
const accountIcon = document.querySelector('#account_icon');
let authCheckVersion = 0;

// Переход на главную страницу по кнопке в шапке.
document.querySelectorAll('.enter_main_page').forEach(button => {
    button.addEventListener('click', () => {
        window.location.href = './index.html';
    });
});

document.querySelectorAll('.account_button').forEach(button => {
    button.addEventListener('click', () => {
        window.location.href = './account_page.html';
    });
});

function updateAuthUI(isAuthenticated) {
    if (authControls) authControls.hidden = isAuthenticated;
    if (accountIcon) accountIcon.hidden = !isAuthenticated;
    if (isAuthenticated) close_user_window();
}

function open_user_window() {
    if (user_window) {
        user_window.hidden = false;
        user_window.classList.add('active');
    }
}

// Подтверждаем авторизацию на сервере, а не по одному наличию токена.
async function checkAuthentication() {
    const version = ++authCheckVersion;
    const token = sessionStorage.getItem('access_token');
    if (!token) {
        updateAuthUI(false);
        return false;
    }

    try {
        await getCurrentAccount(token);
        // Ответ старой проверки не должен отменять новый успешный вход.
        if (version !== authCheckVersion || sessionStorage.getItem('access_token') !== token) return false;
        updateAuthUI(true);
        return true;
    } catch (error) {
        if (version !== authCheckVersion || sessionStorage.getItem('access_token') !== token) return false;
        if (error.status === 401) sessionStorage.removeItem('access_token');
        // При временной ошибке сервера сохраняем токен для повторной проверки.
        updateAuthUI(false);
        return false;
    }
}

// Вход доступен сразу, проверка сохранённого токена выполняется в фоне.
updateAuthUI(false);
checkAuthentication();
window.addEventListener('focus', checkAuthentication);

function close_user_window() {
    if (user_window) {
        user_window.classList.remove('active');
        user_window.hidden = true;
    }
}

const loginForm = document.querySelector("#login-form");
const loginMessage = document.querySelector("#login-message");

if (loginForm && loginMessage) {
    loginForm.addEventListener("input", () => {
        if (loginMessage.dataset.state === "error") {
            loginMessage.textContent = "";
            loginMessage.dataset.state = "";
        }
    });

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const emailOrPhone =
            loginForm.elements.identifier.value.trim();

        const password =
            loginForm.elements.password.value;

        loginMessage.dataset.state = "pending";
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

            loginMessage.dataset.state = "success";
            loginMessage.textContent = "Вход выполнен успешно!";

            authCheckVersion++;
            updateAuthUI(true);
            loginForm.elements.password.value = "";
            accountIcon?.querySelector('.account_button')?.focus();

        } catch (error) {
            loginMessage.dataset.state = "error";
            loginMessage.textContent = error instanceof TypeError
                ? "Не удалось связаться с сервером. Проверьте соединение и попробуйте снова."
                : error.message || "Не удалось выполнить вход";

        } finally {
            submitButton.disabled = false;
        }
    });
}
