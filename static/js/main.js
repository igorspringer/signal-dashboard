const cards = document.getElementById("cards");
const form = document.getElementById("signalForm");

async function loadSignals() {
    const res = await fetch("/api/signals");
    const data = await res.json();

    cards.innerHTML = "";

    data.forEach(s => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <h3>${s.title}</h3>
            <div class="value">${s.value}</div>
            <div class="time">${s.created_at}</div>
        `;
        cards.appendChild(div);
    });
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const value = parseFloat(document.getElementById("value").value);

    await fetch("/api/signals", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, value})
    });

    form.reset();
    loadSignals();
});

loadSignals();
