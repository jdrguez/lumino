const mainContainer = document.getElementById("mainContainer");
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggleButton");

    // Cargar estado inicial del sidebar desde localStorage
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

    // Toggle sidebar al presionar el botón
    toggleButton.addEventListener("click", () => {
      const isVisible = sidebar.style.display !== "none";
      updateLayout(!isVisible);
    });

    // Configuración inicial
    updateLayout(isSidebarVisible);