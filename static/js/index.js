import { updateBookStatus, updateCommentStatus } from "./admin.js";


document.addEventListener("DOMContentLoaded", function () {
    updateBookStatus();
    updateCommentStatus();
});