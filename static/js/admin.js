document.addEventListener("DOMContentLoaded", function () {
    // Ждем, когда весь HTML-документ будет загружен, чтобы выполнить код

    // Добавляем обработчик события для изменения статуса книги
    document.querySelectorAll(".book-switch").forEach(switchElement => {
        // Перебираем все элементы с классом "book-switch"
        switchElement.addEventListener("change", function () {
            // Событие "change" срабатывает, когда переключатель изменяется
            const bookId = this.getAttribute("data-book-id");
            // Получаем уникальный ID книги из атрибута data-book-id
            const isChecked = this.checked;
            // Получаем текущее состояние переключателя (включен или выключен)

            // Отправляем AJAX-запрос на сервер, чтобы изменить статус книги
            fetch(`/change-book-status/${bookId}/`, {
                method: "POST", // Используем POST-запрос для отправки данных
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Добавляем CSRF-токен для защиты запроса
                    "Content-Type": "application/json" // Указываем, что отправляем данные в формате JSON
                },
                body: JSON.stringify({ is_verified: isChecked }) // Отправляем текущее состояние переключателя
            })
            .then(response => response.json()) // Преобразуем ответ в формат JSON
            .then(data => {
                if (data.status !== "success") {
                    // Если статус не "success", выводим сообщение об ошибке
                    alert("Ошибка при обновлении статуса книги");
                }
            });
        });
    });

    // Добавляем обработчик события для изменения статуса комментария
    document.querySelectorAll(".comment-switch").forEach(switchElement => {
        // Перебираем все элементы с классом "comment-switch"
        switchElement.addEventListener("change", function () {
            // Событие "change" срабатывает, когда переключатель изменяется
            const commentId = this.getAttribute("data-comment-id");
            // Получаем уникальный ID комментария из атрибута data-comment-id
            const isChecked = this.checked;
            // Получаем текущее состояние переключателя (включен или выключен)

            // Отправляем AJAX-запрос на сервер, чтобы изменить статус комментария
            fetch(`/change-comment-status/${commentId}/`, {
                method: "POST", // Используем POST-запрос для отправки данных
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"), // Добавляем CSRF-токен для защиты запроса
                    "Content-Type": "application/json" // Указываем, что отправляем данные в формате JSON
                },
                body: JSON.stringify({ is_verified: isChecked }) // Отправляем текущее состояние переключателя
            })
            .then(response => response.json()) // Преобразуем ответ в формат JSON
            .then(data => {
                if (data.status !== "success") {
                    // Если статус не "success", выводим сообщение об ошибке
                    alert("Ошибка при обновлении статуса комментария");
                }
            });
        });
    });

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
});
