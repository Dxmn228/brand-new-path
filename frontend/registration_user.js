const registrationForm = document.querySelector("#registration-form");
const registrationMessage = document.querySelector("#registration-message");

if (registrationForm && registrationMessage) {
    const passwordField = registrationForm.elements.password;
    const confirmationField = registrationForm.elements.password_confirm;
    const registrationButton = registrationForm.querySelector('button[type="submit"]');

    function clearPasswordError() {
        confirmationField.setCustomValidity("");
    }

    passwordField.addEventListener("input", clearPasswordError);
    confirmationField.addEventListener("input", clearPasswordError);

    registrationForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (registrationButton.disabled) return;

        clearPasswordError();
        if (passwordField.value !== confirmationField.value) {
            confirmationField.setCustomValidity("Пароли не совпадают");
            registrationMessage.textContent = "Пароли не совпадают";
            confirmationField.reportValidity();
            return;
        }
        if (!registrationForm.reportValidity()) return;

        const userData = {
            full_name: registrationForm.elements.full_name.value.trim(),
            email: registrationForm.elements.email.value.trim(),
            phone: registrationForm.elements.phone.value.trim(),
            password: passwordField.value,
            password_confirm: confirmationField.value
        };

        registrationButton.disabled = true;
        registrationMessage.textContent = "Выполняется регистрация...";

        try {
            await registerUser(userData);
            registrationMessage.textContent = "Аккаунт создан. Войдите с вашим email и паролем.";
            const loginIdentifier = document.querySelector('#login-form input[name="identifier"]');
            if (loginIdentifier) loginIdentifier.value = userData.email;
            registrationForm.reset();
        } catch (error) {
            registrationMessage.textContent = error.message || "Не удалось зарегистрироваться";
        } finally {
            registrationButton.disabled = false;
        }
    });
}
