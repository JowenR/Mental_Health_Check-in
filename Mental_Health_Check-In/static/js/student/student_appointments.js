// ---------- Cancel appointment (inline confirmation) ----------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-cancel-open]").forEach((openBtn) => {
    const wrap = openBtn.parentElement;
    const confirmForm = wrap.querySelector("[data-cancel-confirm]");
    const closeBtn = wrap.querySelector("[data-cancel-close]");

    openBtn.addEventListener("click", () => {
      openBtn.classList.add("hidden");
      confirmForm.classList.remove("hidden");
    });

    closeBtn.addEventListener("click", () => {
      confirmForm.classList.add("hidden");
      openBtn.classList.remove("hidden");
    });
  });
});
function dismissAlert(el) {
  el.classList.add("opacity-0", "-translate-y-2");
  setTimeout(() => el.remove(), 500);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-alert]").forEach((alert) => {
    const closeBtn = alert.querySelector("[data-alert-close]");
    if (closeBtn) closeBtn.addEventListener("click", () => dismissAlert(alert));
    setTimeout(() => dismissAlert(alert), 8000); // auto-hide after 8 seconds
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("appointment-form");
  const dateInput = document.getElementById("id_date");
  const timeInput = document.getElementById("id_time");
  const bookBtn = document.getElementById("book-btn");

  const calGrid = document.getElementById("cal-grid");
  const calTitle = document.getElementById("cal-title");
  const calPrev = document.getElementById("cal-prev");
  const calNext = document.getElementById("cal-next");
  const dayTpl = document.getElementById("day-template");
  const slotTpl = document.getElementById("slot-template");
  const slotsGrid = document.getElementById("slots-grid");
  const slotsHint = document.getElementById("slots-hint");

  const sumCounselor = document.getElementById("sum-counselor");
  const sumDate = document.getElementById("sum-date");
  const sumTime = document.getElementById("sum-time");

  const MAX_MONTHS_AHEAD = 3;
  const pad = (n) => String(n).padStart(2, "0");
  const toISO = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseISO = (s) => {
    const [y, m, d] = s.split("-").map(Number);
    return new Date(y, m - 1, d);
  };

  const today = parseISO(form.dataset.today);
  let view = new Date(today.getFullYear(), today.getMonth(), 1);
  let timeLabel = "";

  const getCounselorInput = () => form.querySelector('input[name="counselor"]:checked');

  function updateSummary() {
    const c = getCounselorInput();
    sumCounselor.textContent = c ? c.dataset.name : "Not selected";
    sumDate.textContent = dateInput.value
      ? parseISO(dateInput.value).toLocaleDateString("en-US", {
          weekday: "long", month: "long", day: "numeric", year: "numeric",
        })
      : "Not selected";
    sumTime.textContent = timeInput.value ? timeLabel : "Not selected";
    bookBtn.disabled = !(c && dateInput.value && timeInput.value);
  }

  function renderCalendar() {
    calGrid.innerHTML = "";
    calTitle.textContent = view.toLocaleDateString("en-US", { month: "long", year: "numeric" });

    const firstWeekday = new Date(view.getFullYear(), view.getMonth(), 1).getDay();
    const daysInMonth = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();

    for (let i = 0; i < firstWeekday; i++) calGrid.appendChild(document.createElement("span"));

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(view.getFullYear(), view.getMonth(), day);
      const iso = toISO(date);
      const btn = dayTpl.content.firstElementChild.cloneNode(true);
      btn.textContent = day;
      btn.dataset.date = iso;
      btn.disabled = date < today; // past dates can't be picked
      btn.dataset.today = String(iso === toISO(today));
      btn.dataset.selected = String(iso === dateInput.value);
      btn.addEventListener("click", () => selectDate(iso));
      calGrid.appendChild(btn);
    }

    calPrev.disabled = view.getFullYear() === today.getFullYear() && view.getMonth() === today.getMonth();
    const monthsAhead = (view.getFullYear() - today.getFullYear()) * 12 + view.getMonth() - today.getMonth();
    calNext.disabled = monthsAhead >= MAX_MONTHS_AHEAD;
  }

  calPrev.addEventListener("click", () => {
    view = new Date(view.getFullYear(), view.getMonth() - 1, 1);
    renderCalendar();
  });
  calNext.addEventListener("click", () => {
    view = new Date(view.getFullYear(), view.getMonth() + 1, 1);
    renderCalendar();
  });

  function selectDate(iso) {
    dateInput.value = iso;
    timeInput.value = "";
    timeLabel = "";
    renderCalendar();
    loadSlots();
    updateSummary();
  }

  function showHint(text) {
    slotsGrid.classList.add("hidden");
    slotsGrid.innerHTML = "";
    slotsHint.textContent = text;
    slotsHint.classList.remove("hidden");
  }

  async function loadSlots(preselect = "") {
    const c = getCounselorInput();
    if (!c || !dateInput.value) {
      showHint("Select a counselor and a date to see available times.");
      return;
    }
    showHint("Loading available times...");
    try {
      const res = await fetch(`${form.dataset.slotsUrl}?counselor=${c.value}&date=${dateInput.value}`);
      const { slots } = await res.json();

      if (!slots.length) {
        showHint("No available times on this date. Please pick another day.");
        return;
      }

      slotsGrid.innerHTML = "";
      slots.forEach((s) => {
        const btn = slotTpl.content.firstElementChild.cloneNode(true);
        btn.textContent = s.label;
        btn.dataset.value = s.value;
        btn.dataset.selected = String(s.value === preselect);
        if (s.value === preselect) {
          timeInput.value = s.value;
          timeLabel = s.label;
        }
        btn.addEventListener("click", () => {
          timeInput.value = s.value;
          timeLabel = s.label;
          slotsGrid.querySelectorAll("button").forEach((b) =>
            b.setAttribute("data-selected", b === btn ? "true" : "false")
          );
          updateSummary();
        });
        slotsGrid.appendChild(btn);
      });
      slotsHint.classList.add("hidden");
      slotsGrid.classList.remove("hidden");
      updateSummary();
    } catch {
      showHint("Could not load times. Please try again.");
    }
  }

  form.addEventListener("change", (e) => {
    if (e.target.name === "counselor") {
      timeInput.value = "";
      timeLabel = "";
      loadSlots();
      updateSummary();
    }
  });

  const initialDate = form.dataset.date;
  const initialTime = form.dataset.time;
  if (initialDate) {
    const d = parseISO(initialDate);
    view = new Date(d.getFullYear(), d.getMonth(), 1);
    dateInput.value = initialDate;
  }
  renderCalendar();
  if (getCounselorInput() && dateInput.value) loadSlots(initialTime.slice(0, 5));
  updateSummary();
});