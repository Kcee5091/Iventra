
    const showSale = document.getElementById("show-sale-form");
    const saleContainer = document.getElementById("sale-form-container");
    const cancelSale = document.getElementById("cancel-sale");

    showSale.addEventListener("click", () => {
        saleContainer.classList.remove("d-none");
        showSale.classList.add("d-none");
    });

    cancelSale.addEventListener("click", () => {
        saleContainer.classList.add("d-none");
        showSale.classList.remove("d-none");
    });


    const showEdit = document.getElementById("show-edit-form");
    const editContainer = document.getElementById("edit-form-container");
    const cancelEdit = document.getElementById("cancel-edit");

    showEdit.addEventListener("click", () => {
        editContainer.classList.remove("d-none");
        showEdit.classList.add("d-none");
    });

    cancelEdit.addEventListener("click", () => {
        editContainer.classList.add("d-none");
        showEdit.classList.remove("d-none");
    });

if (saleContainer.dataset.hasErrors === "true") {
    saleContainer.classList.remove("d-none");
    showSale.classList.add("d-none");
}

if (editContainer.dataset.hasErrors === "true") {
    editContainer.classList.remove("d-none");
    showEdit.classList.add("d-none");
}

