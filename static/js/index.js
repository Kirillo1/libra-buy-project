import { updateBookStatus, updateCommentStatus } from "./admin.js";
import { likeButtonsHandler, highlightStars } from "./books_view.js";
import { addCartHandler } from "./cart.js";


document.addEventListener("DOMContentLoaded", function () {
    likeButtonsHandler();
    highlightStars();
    updateBookStatus();
    updateCommentStatus();
    addCartHandler();
});