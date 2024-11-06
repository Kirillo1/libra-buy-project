import { getCookie } from "./utils.js";

async function sendAddToCartRequest(bookId) {
  const response = await fetch("/cart/add_to_cart/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `book_id=${bookId}`,
  });
  return await response.json();
}

function handleAddToCartResponse(data) {
  if (data.status === "success") {
    alert(data.message);
  } else {
    alert(data.message);
  }
}

function addCartHandler() {
  document.querySelectorAll(".btn-cart").forEach((button) => {
    button.addEventListener("click", async function () {
      const bookId = this.getAttribute("data-book-id");
      const data = await sendAddToCartRequest(bookId);
      handleAddToCartResponse(data);
    });
  });
}

export { addCartHandler };
