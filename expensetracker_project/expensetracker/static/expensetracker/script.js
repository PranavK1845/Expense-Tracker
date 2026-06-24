document.addEventListener("DOMContentLoaded", function() {
    const navBtns = document.querySelectorAll(".nav-btn");
    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            console.log(`Clicked: ${btn.textContent}`);
        });
    });

    const tableRows = document.querySelectorAll("table tbody tr");
    tableRows.forEach(row => {
        row.addEventListener("mouseenter", () => {
            row.style.backgroundColor = "#f0f8ff";
        });
        row.addEventListener("mouseleave", () => {
            row.style.backgroundColor = "";
        });
    });
});

function addRow() {
    const tableBody = document.querySelector("table tbody");
    if (!tableBody) return;

    const newRow = document.createElement("tr");

    newRow.innerHTML = `
    <td><input type="date" name="date[]"></td>
    <td>
        <select name="category[]">
            <option value="Rent">Rent</option>
            <option value="Groceries">Groceries</option>
            <option value="Education">Education</option>
            <option value="Transport">Transport</option>
            <option value="Entertainment">Entertainment</option>
        </select>
    </td>
    <td><input type="number" name="amount[]" placeholder="Amount"></td>
    <td><input type="text" name="description[]" placeholder="Description"></td>
    <td><button type="button" onclick="removeRow(this)">x</button></td>
`;
    tableBody.appendChild(newRow);
}

function removeRow(button) {
    const row = button.closest("tr");
    if (row) row.remove();
}
