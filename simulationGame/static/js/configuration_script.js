  //Passe das select Element dynamisch nach Breite der atuellen Option an
  
  
  function adjustWidth(selectElement, selectElement0, selectElement1 ) {
    const tempSpan = document.createElement("span");
    tempSpan.style.visibility = "hidden";
    tempSpan.style.position = "absolute";
    tempSpan.style.font = window.getComputedStyle(selectElement).font;
    tempSpan.innerText = selectElement.options[selectElement.selectedIndex].text;
    document.body.appendChild(tempSpan);
    selectElement.style.width = (tempSpan.offsetWidth + 70.34) + "px";
    document.body.removeChild(tempSpan);

    const tempSpan0 = document.createElement("span");
    tempSpan0.style.visibility = "hidden";
    tempSpan0.style.position = "absolute";
    tempSpan0.style.font = window.getComputedStyle(selectElement0).font;
    tempSpan0.innerText = selectElement0.options[selectElement0.selectedIndex].text;
    document.body.appendChild(tempSpan0);
    selectElement0.style.width = (tempSpan0.offsetWidth + 70.34) + "px";
    document.body.removeChild(tempSpan0);

    const tempSpan1 = document.createElement("span");
    tempSpan1.style.visibility = "hidden";
    tempSpan1.style.position = "absolute";
    tempSpan1.style.font = window.getComputedStyle(selectElement1).font;
    tempSpan1.innerText = selectElement1.options[selectElement1.selectedIndex].text;
    document.body.appendChild(tempSpan1);
    selectElement1.style.width = (tempSpan1.offsetWidth + 70.34) + "px";
    document.body.removeChild(tempSpan1);
  }

  // Beim ersten Laden aufrufen
  window.addEventListener("load", ()=> {
    const select = document.getElementById("dynamicSelect");
    const select0 = document.getElementById("dynamicSelect0");
    const select1 = document.getElementById("dynamicSelect1");
    adjustWidth(select, select0, select1);
  });
function toggleTooltip() {
  const container = document.querySelector('.tooltip-container');
  container.classList.toggle('show');
}



//Animate den Rad

  const { animate, text, stagger,svg } = anime;
      animate('.bi-gear-fill', {
      rotate: { to: '1turn' },  // -1turn für Gegenrichtung
      ease: 'linear',           // gleichmäßige Geschwindigkeit
      duration: 2000,            // 2s pro Umdrehung (größer = langsamer)
      loop: true,
      delay:1000
    });
