"use strict";
document.documentElement.classList.add("js");
(() => {
  const data = JSON.parse(document.getElementById("site-data").textContent);
  const ui = data.ui;
  const reader = document.getElementById("reader");
  const audio = document.getElementById("narration");
  const image = document.getElementById("reader-image");
  const text = document.getElementById("reader-text");
  const previous = document.getElementById("reader-prev");
  const next = document.getElementById("reader-next");
  const play = document.getElementById("audio-toggle");
  const error = document.getElementById("audio-error");
  let book = null;
  let page = 0;
  let lastTrigger = null;
  let touch = null;
  let playAttempt = 0;

  function open(dialog, trigger) {
    lastTrigger = trigger;
    dialog.showModal();
    dialog.scrollTop = 0;
  }

  document.querySelectorAll("[data-open-languages]").forEach(button => {
    button.addEventListener("click", () => open(document.getElementById("languages"), button));
  });
  document.querySelectorAll("[data-open-credits]").forEach(button => {
    button.addEventListener("click", () => open(document.getElementById("credits"), button));
  });
  document.querySelectorAll("[data-close-dialog]").forEach(button => {
    button.addEventListener("click", () => button.closest("dialog").close());
  });
  document.querySelectorAll("dialog").forEach(dialog => {
    dialog.addEventListener("click", event => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    });
    dialog.addEventListener("close", () => {
      if (dialog === reader) stopAudio();
      lastTrigger?.focus({preventScroll: true});
    });
  });

  function clock(seconds) {
    if (!Number.isFinite(seconds)) return "0:00";
    return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  }

  function syncAudio() {
    const playing = !audio.paused && !audio.ended;
    document.getElementById("audio-label").textContent = playing ? ui.pause : ui.listen;
    document.getElementById("audio-icon").textContent = playing ? "Ⅱ" : "▶";
    play.setAttribute("aria-label", playing ? ui.pause : ui.listen);
    play.setAttribute("aria-pressed", String(playing));
    document.getElementById("audio-time").textContent = `${clock(audio.currentTime)} / ${clock(audio.duration)}`;
  }

  function stopAudio() {
    playAttempt += 1;
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
    syncAudio();
  }

  function render() {
    stopAudio();
    error.hidden = true;
    const current = book.pages[page];
    image.src = `../${current.image}`;
    image.alt = `${book.title} — ${page + 1} / ${book.pages.length}`;
    document.getElementById("reader-image-label").textContent = `${String(page + 1).padStart(2,"0")} / ${String(book.pages.length).padStart(2,"0")}`;
    text.textContent = current.text;
    document.getElementById("reader-count").textContent = `${page + 1} / ${book.pages.length}`;
    document.getElementById("reader-count").setAttribute("aria-label", `${ui.page} ${page + 1} / ${book.pages.length}`);
    previous.disabled = page === 0;
    next.disabled = page === book.pages.length - 1;
    document.getElementById("reader-end").hidden = page !== book.pages.length - 1;
    audio.src = `../${current.audio}`;
    audio.load();
    if (book.pages[page + 1]) {
      const preload = new Image();
      preload.src = `../${book.pages[page + 1].image}`;
    }
  }

  function turn(direction) {
    const target = page + direction;
    if (!book || target < 0 || target >= book.pages.length) return;
    const focused = document.activeElement;
    page = target;
    render();
    // Keep keyboard focus inside the active navigation controls at either end.
    if (focused === next && next.disabled) previous.focus({preventScroll:true});
    if (focused === previous && previous.disabled) next.focus({preventScroll:true});
  }

  document.querySelectorAll("[data-book]").forEach(button => {
    button.addEventListener("click", () => {
      book = data.books.find(candidate => candidate.id === button.dataset.book);
      if (!book) return;
      page = 0;
      document.getElementById("reader-title").textContent = book.title;
      document.getElementById("reader-series").textContent = book.series === "popo" ? "POPO, MUMU & NEMU" : "MALLOW TOWN";
      document.getElementById("reader-level").textContent = `LEVEL ${book.level} · ENGLISH`;
      document.getElementById("reader-credit").textContent = `© 2026 ${book.author} · ${book.license}`;
      render();
      open(reader, button);
    });
  });
  previous.addEventListener("click", () => turn(-1));
  next.addEventListener("click", () => turn(1));
  play.addEventListener("click", async () => {
    if (!audio.paused) { audio.pause(); return; }
    error.hidden = true;
    const attempt = ++playAttempt;
    if (audio.ended) audio.currentTime = 0;
    try { await audio.play(); }
    catch (exception) {
      if (attempt === playAttempt && exception.name !== "AbortError") error.hidden = false;
    }
  });
  ["play", "pause", "ended", "timeupdate", "loadedmetadata", "emptied"].forEach(name => audio.addEventListener(name, syncAudio));
  audio.addEventListener("error", () => { if (reader.open && audio.hasAttribute("src")) error.hidden = false; });
  document.addEventListener("visibilitychange", () => { if (document.hidden) audio.pause(); });
  reader.addEventListener("keydown", event => {
    if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
      event.preventDefault();
      turn(event.key === "ArrowRight" ? 1 : -1);
    }
  });
  const art = document.querySelector(".reader-image-wrap");
  art.addEventListener("touchstart", event => {
    touch = {x:event.changedTouches[0].clientX, y:event.changedTouches[0].clientY};
  }, {passive:true});
  art.addEventListener("touchend", event => {
    if (!touch) return;
    const dx = event.changedTouches[0].clientX - touch.x;
    const dy = event.changedTouches[0].clientY - touch.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4) turn(dx < 0 ? 1 : -1);
    touch = null;
  }, {passive:true});
  document.querySelectorAll(".language-grid a").forEach(link => {
    link.addEventListener("click", () => {
      try { localStorage.setItem("storyleaf-language", link.lang); } catch (_) { /* Storage is optional. */ }
    });
  });
})();
