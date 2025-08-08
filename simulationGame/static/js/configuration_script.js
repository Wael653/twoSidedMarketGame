  //Passe das select Element dynamisch nach Breite der atuellen Option an
  function adjustWidth(selectElement) {
    const tempSpan = document.createElement("span");
    tempSpan.style.visibility = "hidden";
    tempSpan.style.position = "absolute";
    tempSpan.style.font = window.getComputedStyle(selectElement).font;
    tempSpan.innerText = selectElement.options[selectElement.selectedIndex].text;
    document.body.appendChild(tempSpan);
    selectElement.style.width = (tempSpan.offsetWidth + 70.34) + "px";
    document.body.removeChild(tempSpan);
  }

  // Beim ersten Laden aufrufen
  window.addEventListener("load", ()=> {
    const select = document.getElementById("dynamicSelect");
    adjustWidth(select);
  });
   function toggleTooltip() {
    const tooltip = document.getElementById('tooltip-text');
    const icon = document.getElementById('icon')
    tooltip.classList.toggle('show');
    icon.classList.toggle('show');
  }




