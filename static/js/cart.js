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

async function sendRemoveFromCartRequest(cartBookId) {
  const response = await fetch(`/cart/remove_from_cart/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `cart_book_id=${cartBookId}`,
  });
  return response.json();
}

function handleRemoveFromCartResponse(data, cartBookId) {
  if (data.status === "success") {
    document.querySelector(`[data-cart-book-id="${cartBookId}"]`).closest(".col-12").remove();
    alert(data.message);
  } else {
    alert(data.message);
  }
}

function removeCartHandler() {
  document.querySelectorAll(".btn-remove-cart").forEach((button) => {
    button.addEventListener("click", function () {
      const cartBookId = this.getAttribute("data-cart-book-id");
      sendRemoveFromCartRequest(cartBookId).then((data) => handleRemoveFromCartResponse(data, cartBookId));
    });
  });
}

export { addCartHandler, removeCartHandler };
