  //Passe das select Element dynamisch nach Breite der atuellen Option an
  
  
  function adjustWidth(selectElement, selectElement0) {
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
  }

  // Beim ersten Laden aufrufen
  window.addEventListener("load", ()=> {
    const select = document.getElementById("dynamicSelect");
    const select0 = document.getElementById("dynamicSelect0");
    adjustWidth(select, select0);
  });
function toggleTooltip() {
  const tip  = document.getElementById('tooltip-text');
  const icon = document.getElementById('icon23');

  tip.classList.toggle('show');
  icon.classList.toggle('show');

  if (tip.classList.contains('show')) {
    positionTooltipByCard(tip);   // <-- jetzt wirklich ausrichten
  }
}


function positionTooltipByCard(tip){
  // Reset: zentriert + Breite an Card clampen
  tip.classList.remove('align-start','align-end');

  const card = tip.closest('.custom-modal-content');
  const cs   = getComputedStyle(card);
  const pad  = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);

  tip.style.maxWidth = (card.clientWidth - pad) + 'px';

  // Nach dem Clampen prüfen, ob wir über Card-Kanten ragen:
  const cRect = card.getBoundingClientRect();
  const tRect = tip.getBoundingClientRect();
  const m = 4; // kleiner Sicherheitsrand

  if (tRect.right > cRect.right - m) {
    tip.classList.add('align-end');    // an rechte Card-Kante
  } else if (tRect.left < cRect.left + m) {
    tip.classList.add('align-start');  // an linke Card-Kante
  }
}

// Bei Resize neu ausrichten, wenn sichtbar
window.addEventListener('resize', () => {
  const tip = document.getElementById('tooltip-text');
  if (tip && tip.classList.contains('show')) positionTooltipByCard(tip);
});


//Animate den Rad
  const { animate, text, stagger,svg } = anime;
      animate('.bi-gear-fill', {
      rotate: { to: '1turn' },  // -1turn für Gegenrichtung
      ease: 'linear',           // gleichmäßige Geschwindigkeit
      duration: 2000,            // 2s pro Umdrehung (größer = langsamer)
      loop: true,
      delay:1000
    });


function positionTooltip(tip) {
  // reset auf Standard (zentriert)
  tip.classList.remove('align-start','align-end');
  tip.style.maxWidth = ''; 

  const wrapper   = tip.parentElement;                 // .tooltip-wrapper
  const wRect     = wrapper.getBoundingClientRect();
  const vw        = window.innerWidth;
  const margin    = 8;                                 // Sicherheitsrand
  const vwMax     = vw - 2*margin;                     // max. Viewportbreite

  // immer auf Viewport begrenzen
  tip.style.maxWidth = vwMax + 'px';

  // nach Zentrierung messen
  let rect = tip.getBoundingClientRect();

  const spaceRight = vw - wRect.left  - margin;        // Platz rechts vom Icon
  const spaceLeft  = wRect.right       - margin;       // Platz links  vom Icon

  // Wenn rechts übersteht und links mehr Platz hat -> rechts andocken
  if (rect.right > vw - margin && spaceLeft > spaceRight) {
    tip.classList.add('align-end');
    tip.style.maxWidth = Math.min(vwMax, spaceLeft) + 'px';
  }
  // Wenn links übersteht und rechts >= Platz -> links andocken
  else if (rect.left < margin && spaceRight >= spaceLeft) {
    tip.classList.add('align-start');
    tip.style.maxWidth = Math.min(vwMax, spaceRight) + 'px';
  }
}
