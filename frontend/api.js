const API_URL = "http://localhost:8000"; // адрес backend'а
// открываем frontend и backend на одном устройстве

// Вход пользователя или организации
async function loginUser(emailOrPhone, password) {
    const formData = new URLSearchParams();

    // FastAPI OAuth2PasswordRequestForm ожидает
    // поля username и password в form-urlencoded
    formData.set("username", emailOrPhone);
    formData.set("password", password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const detail = data?.detail;
        const message = response.status === 401
            ? "Неверный email, телефон или пароль. Проверьте данные и попробуйте снова."
            : Array.isArray(detail)
                ? detail.map(error => error.msg).join("; ")
                : typeof detail === "string" ? detail : "Не удалось выполнить вход. Попробуйте позже.";
        const error = new Error(message);
        error.status = response.status;
        throw error;
    }

    return data;
}

// Регистрация пользователя. Названия полей соответствуют UserRegister.
async function registerUser(userData) {
    const response = await fetch(`${API_URL}/auth/register/user`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        const detail = data?.detail;
        const message = Array.isArray(detail)
            ? detail.map(error => error.msg).join("; ")
            : typeof detail === "string" ? detail : `Ошибка сервера: ${response.status}`;
        throw new Error(message);
    }

    return data;
}

// Backend проверяет подпись и срок действия токена, затем ищет аккаунт в БД.
async function getCurrentAccount(token) {
    const response = await fetch(`${API_URL}/auth/me`, {
        headers: { "Authorization": `Bearer ${token}` },
        cache: "no-store"
    });

    if (!response.ok) {
        const error = new Error("Не удалось проверить вход в аккаунт");
        error.status = response.status;
        throw error;
    }

    return response.json();
}

// Проверка доступности backend
async function checkBackend() {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
        throw new Error("Backend недоступен");
    }

    return response.json();
}
