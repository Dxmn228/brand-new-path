// Общая разметка входа и регистрации. Подключать перед enter_user.js и registration_user.js.
if (!document.getElementById('user_window')) {
    document.body.insertAdjacentHTML('beforeend', String.raw`
    <div id="user_window" class="user_window" hidden>
        <p class="background"></p>
        <p class="exit">Выйти</p>
        <div class="log_in">
            <p class="log_in_enter">Вход</p>
            <p class="log_in_text">Войдите в профиль с помощью email или телефона (на выбор) и пароля</p>
            <form id ="login-form">
            <input
                type="text"
                name="identifier"
                placeholder="Email или номер телефона"
                class="log_in_email_or_phone_number"
                autocomplete="username"
                minlength="11"
                maxlength="25"
                aria-describedby="login-message"
                required
            >
            <input
                type="password"
                name="password"
                placeholder="Пароль"
                class="log_in_password"
                autocomplete="current-password"
                minlength="8"
                maxlength="25"
                aria-describedby="login-message"
                required
            >
            <button type="submit" class="log_in_submit">Войти</button>
            <p id="login-message" role="status" aria-live="polite" aria-atomic="true"></p>
            </form>
        </div>
        <div class="registration">
            <p class="registration_task">Регистрация</p>
            <p class="registration_text">Зарегестрируйте свой профиль, используя свое имя, email и номер телефона</p>
            <form id="registration-form" method="post">
            <input
                type="text"
                name="full_name"
                placeholder="Ваше имя"
                class="registration_name"
                autocomplete="name"
                minlength="1"
                maxlength="25"
                required
            >
            <input
                type="email"
                name="email"
                placeholder="Ваш email"
                class="registration_email"
                autocomplete="email"
                minlength="11"
                maxlength="25"
                required
            >
            <input
                type="tel"
                name="phone"
                placeholder="+79991234567"
                class="registration_phone"
                autocomplete="tel"
                pattern="\+7[0-9]{10}"
                minlength="12"
                maxlength="12"
                required
            >
            <p class="password_first">Введите пароль в первом поле и повторите во втором</p>
            <input
                type="password"
                name="password"
                placeholder="Введите свой пароль"
                class="registration_password"
                autocomplete="new-password"
                minlength="8"
                maxlength="25"
                required
            >
            <input
                type="password"
                name="password_confirm"
                placeholder="Повторите свой пароль"
                class="repeat_password"
                autocomplete="new-password"
                minlength="8"
                maxlength="25"
                required
            >
            <button type="submit" class="registration_submit">Зарегистрироваться</button>
            <p id="registration-message" role="status" aria-live="polite"></p>
            </form>
        </div>
        <button class="exit_button" onclick="close_user_window()"></button>
    </div>
    `);
}
