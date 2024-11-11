import {
    updateBookStatus,
    updateCommentStatus,
    addChangeEventToSelect 
} from "./admin.js";
import { likeButtonsHandler, highlightStars } from "./books_view.js";
import { addCartHandler, removeCartHandler } from "./cart.js";


document.addEventListener("DOMContentLoaded", function () {
    likeButtonsHandler();
    highlightStars();
    updateBookStatus();
    updateCommentStatus();
    addCartHandler();
    removeCartHandler();
    addChangeEventToSelect();
});