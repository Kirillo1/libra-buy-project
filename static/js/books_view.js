import { getCookie } from "./utils.js";

function highlightStars() {
  document.querySelectorAll(".rating-stars").forEach(starsContainer => {
    const avgRating = parseFloat(starsContainer.getAttribute("data-avg-rating"));
    const stars = starsContainer.querySelectorAll(".star");
    
    stars.forEach((star, index) => {
      // Подсвечиваем звезды, если индекс звезды меньше среднего рейтинга
      if (index < avgRating) {
        star.classList.add("active"); // Добавьте класс для подсвечивания, например, 'active'
      } else {
        star.classList.remove("active");
      }
    });
  });
}

function likeButtonsHandler() {
  document.querySelectorAll(".rating-stars").forEach(starsContainer => {
    starsContainer.querySelectorAll(".star").forEach(star => {
      star.addEventListener("click", function () {
        const score = this.getAttribute("data-score");
        const bookId = this.getAttribute("data-book-id");

        fetch(`/book/${bookId}/rate/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: `score=${score}`
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === "success") {
            document.getElementById(`average-rating-${bookId}`).textContent = data.average_rating.toFixed(2);
            starsContainer.setAttribute("data-avg-rating", data.average_rating);
            highlightStars();
          } else {
            alert(data.message);
          }
        });
      });
    });
  });
}

export {
  likeButtonsHandler,
  highlightStars,
};
