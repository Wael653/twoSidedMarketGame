let chartsInited = false;
function initChartsOnce() {
  if (chartsInited) return;
  chartsInited = true;
    const ctxSupplier = document.getElementById('chart-supplier');
    const ctxBuyer = document.getElementById('chart-buyer');
    const ctxSales = document.getElementById('chart-sales');
    roundsLabel = []
    let roundNumber = document.getElementById("round_header")
    data = roundNumber.dataset
    for (let i = 1; i < Number(data.roundNumber) + 1; i++) {
    roundsLabel.push("Runde " + i);
    } 
    /** Extrahiere Supplierdaten */
    const suppliersData = document.getElementById("suppliers_data");

    // Extrahiere Anzahl der Verkäufer aus Flohemarkt A
    const suppliersRawA = suppliersData.dataset.suppliersA; 
    const suppliersNumberA = suppliersRawA.split(',').map(item => Number(item));

    // Extrahiere Anzahl der Verkäufer aus Flohemarkt B
    const suppliersRawB = suppliersData.dataset.suppliersB; 
    const suppliersNumberB = suppliersRawB.split(',').map(item => Number(item));

    //Extrahiere die Standmieten pro Runde aus Flohmarkt A  
    const standRentalsRawA = suppliersData.dataset.supplierPricesListA;
    const standRentalsA = standRentalsRawA.split(',').map(item => Number(item));

    //Extrahiere die Standmieten pro Runde aus Flohmarkt B 
    const standRentalsRawB = suppliersData.dataset.supplierPricesListB;
    const standRentalsB = standRentalsRawB.split(',').map(item => Number(item));


    /** Extrahiere Buyerdaten */
    const buyersData = document.getElementById("buyers_data");

    // Extrahiere Anzahl der Käufer aus Flohemarkt A
    const buyersRawA = buyersData.dataset.buyersA; 
    const buyersNumberA = buyersRawA.split(',').map(item => Number(item));

    // Extrahiere Anzahl der käufer aus Flohemarkt B
    const buyersRawB = buyersData.dataset.buyersB; 
    const buyersNumberB = buyersRawB.split(',').map(item => Number(item));

    //Extrahiere die Eintrittsgebühren pro Runde aus Flohmarkt A  
    const entranceFeesRawA = buyersData.dataset.buyerPricesListA;
    const entranceFeesA = entranceFeesRawA.split(',').map(item => Number(item));

    //Extrahiere die Eintrittsgebühren pro Runde aus Flohmarkt B 
    const entranceFeesRawB = buyersData.dataset.buyerPricesListB;
    const entranceFeesB = entranceFeesRawB.split(',').map(item => Number(item));

    /** Extrahiere Umsatzdaten */
    const salesData = document.getElementById("sales-data");

    // Flohmarkt A
    const salesRawA = salesData.dataset.salesA; 
    const salesA = salesRawA.split(',').map(item => Number(item));

    //Flohmarkt B
    const salesRawB = salesData.dataset.salesB; 
    const salesB = salesRawB.split(',').map(item => Number(item));
    
    //Teste die gespeicherten Daten
    console.log("Anzahl der Käufer in A: " ,buyersNumberA)
    console.log("round_number + 1: ", roundNumber.dataset.roundNumber + 1)
    console.log("Seite wurde geladen")
    console.log(roundNumber.dataset)
    console.log("roundsLabel: ", roundsLabel)
    console.log("suppliersDataSet: ", suppliersData.dataset)
    console.log("suppliersNumberRawA: ", suppliersData.dataset.suppliersA)
    console.log("suppliersNumberRawB: ", suppliersData.dataset.suppliersB)
    console.log("standRentalsRawA: ", standRentalsRawA)
    console.log("standRentalsA: ", standRentalsA)
    console.log("salesA: ", salesA)
    console.log("salesB: ", salesB)
    new Chart(ctxSupplier, {
        type: 'bar',
        data: {
            labels: roundsLabel,
            datasets: [
                {
                    label: 'Anzahl der Verkäufer in Flohmarkt A',
                    data: suppliersNumberA, 
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                },
                {
                    label: 'Anzahl der Verkäufer in Flohmarkt B',
                    data: suppliersNumberB,
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                }
            ]
        },
        options: {
            responsive: true,
            /* maintainAspectRatio: false, */
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    ticks: {
                        color: '#25c46dff',         // Schriftfarbe
                        font: {
                            size: 16,          // Schriftgröße
                            family: 'Arial',   // Schriftart
                            weight: 400             // Schriftstil
                            }
            }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function (contexts) {
                            const roundIndex = contexts[0].dataIndex;
                            return `Runde ${roundIndex + 1}`;
                        },
                        // Inhalt pro Balken (A oder B)
                        label: function (context) {
                            const index = context.dataIndex; // Rundenindex
                            const datasetIndex = context.datasetIndex; // Speichere den Index
                            const datasetLabel = context.dataset.label;

                            // Verkäuferanzahl des aktuellen Balkens
                            const anzahl = context.raw;

                            const preis = datasetIndex === 0
                                ? standRentalsA[index]
                                : standRentalsB[index];

                            // Rückgabe als zusammengesetzter String
                            return [`${datasetLabel}: ${anzahl}`,
                                `Standmiete : ${preis} €`
                            ]
                        }
                    }
                }
            }
        }
    });

    new Chart(ctxBuyer, {
        type: 'bar',
        data: {
            labels: roundsLabel,
            datasets: [
                {
                    label: 'Anzahl der Käufer in Flohmarkt A',
                    data: buyersNumberA,
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                },
                {
                    label: 'Anzahl der Käufer in Flohmarkt B',
                    data: buyersNumberB,
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    ticks: {
                        color: '#25c46dff',         // Schriftfarbe
                        font: {
                            size: 16,          // Schriftgröße
                            family: 'Arial',   // Schriftart
                            weight: 400             // Schriftstil
                            }
            }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function (contexts) {
                            const roundIndex = contexts[0].dataIndex;
                            return `Runde ${roundIndex + 1}`;
                        },
                        label: function (context) {
                            const index = context.dataIndex;
                            const datasetIndex = context.datasetIndex;
                            const datasetLabel = context.dataset.label;

                            const anzahl = context.raw;
                            const preis = datasetIndex === 0
                                ? entranceFeesA[index]
                                : entranceFeesB[index];

                            return [
                                `${datasetLabel}: ${anzahl}`,
                                `Eintrittsgebühr : ${preis} €`
                            ];
                        }
                    }
                }
            }
        }
    });

    //Chart Umsätze 
    new Chart(ctxSales, {
        type: 'bar',
        data: {
            labels: roundsLabel,
            datasets: [
                {
                    label: 'Umsatz von Flohmarkt A',
                    data: salesA,
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                },
                {
                    label: 'Umsatz von Flohmarkt B',
                    data: salesB,
                    borderWidth: 2,
                    barPercentage: 0.4,
                    categoryPercentage: 0.6
                }
            ]
        },
        options: {
            responsive: true,
            /* maintainAspectRatio: false, */
            scales: {
                y: {
                    beginAtZero: true
                },
                   x: {
                    ticks: {
                        color: '#25c46dff',         // Schriftfarbe
                        font: {
                            size: 16,          // Schriftgröße
                            family: 'Arial',   // Schriftart
                            weight: 400             // Schriftstil
                            }
            }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function (contexts) {
                            const roundIndex = contexts[0].dataIndex;
                            return `Runde ${roundIndex + 1}`;
                        },
                        // Inhalt pro Balken (A oder B)
                        label: function (context) {
                            const index = context.dataIndex; // Rundenindex
                            const datasetIndex = context.datasetIndex; // Speichere den Index
                            const datasetLabel = context.dataset.label;

                            // Umsatz des aktuellen Balkens
                            const sale = context.raw;

                            const preis = datasetIndex === 0
                                ? salesA[index]
                                : salesB[index];

                            // Gebe den zusammengesetzten String zurück
                            return [`${datasetLabel}: ${sale}`,
                                
                            ]
                        }
                    }
                }
            }
        }
    });


}



// Toggle Balkendiagramme beim Klick auf den Anzeige-Button
const btn2 = document.getElementById("toggle-charts")
btn2.addEventListener("click", ()=>{
    const chartsContainer = document.getElementById("charts-container-id");
    if (!chartsInited) initChartsOnce();
//    chartsContainer.classList.toggle('hidden');
    chartsContainer.classList.toggle('visible');
    if (chartsContainer.classList.contains('visible')) {
        btn2.innerHTML = '<i class="bi bi-bar-chart-line-fill"></i> Diagramme ausblenden'
    }
    else {
        btn2.innerHTML = '<i class="bi bi-bar-chart-line-fill"></i> Diagramme anzeigen'
    }
});

//Animation
  window.addEventListener('DOMContentLoaded', () => {
    const { animate, utils } = anime;

    document.querySelectorAll('.count[data-target]').forEach(element => {
      const to      = Number(element.dataset.target) || 0;
      const suffix  = element.dataset.suffix || '';
      const prefix  = element.dataset.prefix || '';
      const roundN  = Number(element.dataset.round || 0);  // 0 = ganze Zahlen

      const state = { v: 0 };
      animate(state, {
        v: to,
        duration: 1500,
        ease: 'linear',
        modifier: utils.round(roundN),
        onUpdate: () => {
          element.textContent = `${prefix}${state.v}${suffix}`;
        }
      });
    });
  });



