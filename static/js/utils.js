// Функция для получения CSRF-токена из cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        // Проверяем, есть ли куки
        const cookies = document.cookie.split(";");
        // Разделяем куки на отдельные элементы
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Удаляем пробелы в начале и конце строки куки
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                // Проверяем, если название куки совпадает с переданным именем
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // Извлекаем значение куки и декодируем его
                break;
            }
        }
    }
    return cookieValue; // Возвращаем найденный CSRF-токен
}

export {
    getCookie,
};