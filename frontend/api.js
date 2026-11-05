const API_URL = "http://localhost:8000"; // адрес backend'а
// открываем frontend и backend на одном устройстве

// Вход пользователя или организации
async function loginUser(emailOrPhone, password) {
    const formData = new URLSearchParams();

    // FastAPI OAuth2PasswordRequestForm ожидает
    // поля username и password в form-urlencoded.
    formData.set("username", emailOrPhone);
    formData.set("password", password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || `Ошибка сервера: ${response.status}`
        );
    }

    return data;
}

// Проверка доступности backend
async function checkBackend() {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
        throw new Error("Backend недоступен");
    }

    return response.json();
}
