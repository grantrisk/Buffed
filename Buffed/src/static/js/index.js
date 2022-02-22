let currentDate = new Date();
const MONTHS = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
document.getElementById("date-text").innerText = `${MONTHS[currentDate.getMonth()]} ${currentDate.getDate()}` +
    `, ${currentDate.getFullYear()}`;