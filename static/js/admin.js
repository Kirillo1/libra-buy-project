import { getCookie } from "./utils.js";

function updateBookStatus() {
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
}

function updateCommentStatus() {
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
}


export {
    updateBookStatus,
    updateCommentStatus
}
