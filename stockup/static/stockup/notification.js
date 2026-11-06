const notifications = document.querySelectorAll(".notification");

notifications.forEach((notification) => {

    function removeNotification() {
        if (notification.classList.contains("removing")) return;

        notification.classList.add("removing");

        notification.addEventListener("animationend", () => {
            notification.remove();
        }, { once: true });
    }

    const closeButton = notification.querySelector(".notification-close");

    closeButton.addEventListener("click", removeNotification);

    setTimeout(removeNotification, 4000);

});