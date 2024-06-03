function toggleBalanceDetails(balanceId) {
    var details = document.getElementById(balanceId);
    if (details.style.display === "none") {
        details.style.display = "block";
    } else {
        details.style.display = "none";
    }
}