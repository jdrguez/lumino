document.addEventListener("DOMContentLoaded", function () {
  // Botón para el sidebar
  const mainContainer = document.getElementById("mainContainer");
  const sidebar = document.getElementById("sidebar");
  const toggleButton = document.getElementById("toggleButton");
  const isSidebarVisible = localStorage.getItem("isSidebarVisible") !== "false";

  function updateLayout(showSidebar) {
    if (showSidebar) {
      mainContainer.classList.remove("full");
      sidebar.style.display = "block";
    } else {
      mainContainer.classList.add("full");
      sidebar.style.display = "none";
    }
    localStorage.setItem("isSidebarVisible", showSidebar);
  }

  toggleButton.addEventListener("click", () => {
    const isVisible = sidebar.style.display !== "none";
    updateLayout(!isVisible);
  });
  updateLayout(isSidebarVisible);

  // Duración de las alertas django
  const messages = document.querySelectorAll(".alert");
  console.log(messages);
  const fadeInDuration = 1000;
  const fadeOutDuration = 1000;
  const displayDuration = 3000;

  messages.forEach((message) => {
    message.style.opacity = 0;
    message.style.display = "block";
    let fadeIn = setInterval(() => {
      if (parseFloat(message.style.opacity) < 1) {
        message.style.opacity = (parseFloat(message.style.opacity) || 0) + 0.1;
      } else {
        clearInterval(fadeIn);
      }
    }, fadeInDuration / 10);

    setTimeout(() => {
      let fadeOut = setInterval(() => {
        if (parseFloat(message.style.opacity) > 0) {
          message.style.opacity -= 0.1;
        } else {
          clearInterval(fadeOut);
          message.style.display = "none";
        }
      }, fadeOutDuration / 10);
    }, displayDuration);
  });

  // Botón de cerrar mensaje

  const btn = document.getElementById("close-btn");
  const mark = document.getElementById("mark-display");
  btn.addEventListener("click", () => {
    mark.style.display = "none";
  });
});
