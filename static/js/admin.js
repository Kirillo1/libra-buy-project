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

// Получение данных заказа из выбранного элемента
function getSelectedOrderData(selectElement) {
    const orderId = selectElement.getAttribute("data-order-id");
    const paymentStatus = selectElement.value;
    return { orderId, paymentStatus };
  }
  
  // Отправка AJAX-запроса для обновления статуса оплаты
  function sendUpdatePaymentStatusRequest(orderId, paymentStatus) {
    return fetch(`/update_payment_status/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        order_id: orderId,
        payment_status: paymentStatus,
      }),
    }).then(response => response.json());
  }
  
  
  // Обработка ответа от сервера
  function handleResponse(data) {
    if (data.status === "success") {
      alert("Статус оплаты успешно обновлен");
    } else {
      alert("Ошибка при обновлении статуса оплаты");
    }
  }
  
  // Добавление обработчика события изменения к каждому селекту
  function addChangeEventToSelect() {
    document.querySelectorAll(".form-select").forEach(select => {
      select.addEventListener("change", function () {
        const { orderId, paymentStatus } = getSelectedOrderData(this);
        sendUpdatePaymentStatusRequest(orderId, paymentStatus)
          .then(handleResponse)
          .catch(error => console.error("Ошибка:", error));
      });
    });
  }
  

export {
    updateBookStatus,
    updateCommentStatus,
    addChangeEventToSelect,
}
