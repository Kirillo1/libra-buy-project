import { updateBookStatus, updateCommentStatus } from "./admin.js";
import { likeButtonsHandler, highlightStars } from "./books_view.js";


document.addEventListener("DOMContentLoaded", function () {
    likeButtonsHandler();
    highlightStars();
    updateBookStatus();
    updateCommentStatus();
});