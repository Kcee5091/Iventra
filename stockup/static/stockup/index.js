const loadMoreButton = document.getElementById("load-more-sales");
const historyList = document.getElementById("sales-history-list");
const endMessage = document.getElementById("sales-end-message");

if (loadMoreButton) {

    loadMoreButton.addEventListener("click", async function () {

        const url = this.dataset.url;
        const page = this.dataset.page;

        this.disabled = true;
        this.textContent = "Loading...";

        try {

            const response = await fetch(`${url}?page=${page}`);

            if (!response.ok) {
                throw new Error("Could not load sales history.");
            }

            const data = await response.json();
            

            

            const startIndex = historyList.children.length;

            historyList.insertAdjacentHTML("beforeend", data.html);

            const newRows = Array.from(historyList.children).slice(startIndex);

            newRows.forEach((row, index) => {
                row.style.animationDelay = `${index * 60}ms`;
            });


            if (data.has_next) {

                this.dataset.page = Number(page) + 1;
                this.disabled = false;
                this.textContent = "Load More";

            } else {

                this.remove();
                endMessage.classList.remove("d-none");

            }

        } catch (error) {

            console.error(error);

            this.disabled = false;
            this.textContent = "Try Again";

        }

    });

}
