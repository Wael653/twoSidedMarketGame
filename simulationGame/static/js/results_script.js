const ctx = document.getElementById('myChart');
roundsLabel = []
let roundNumber = document.getElementById("round_header")
data = roundNumber.dataset
for (let i = 1; i < Number(data.roundNumber) + 1; i++) {
  roundsLabel.push("Runde " + i);
} 
/** Extrahiere Supplierdaten */
const suppliersData = document.getElementById("suppliers_data");
// Extrahiere Daten aus Flohemarkt A
const suppliersRawA = suppliersData.dataset.suppliersA; 
const suppliersNumberA = suppliersRawA.split(',').map(item => Number(item));

// Extrahiere Daten aus Flohemarkt B
const suppliersRawB = suppliersData.dataset.suppliersB; 
const suppliersNumberB = suppliersRawB.split(',').map(item => Number(item));

//Extrahiere die Preise pro Runde aus Flohmarkt A  
const pricesPerRoundRawA = suppliersData.dataset.pricesListA;
const pricesPerRoundA = pricesPerRoundRawA.split(',').map(item => Number(item));

//Extrahiere die Preise pro Runde aus Flohmarkt B 
const pricesPerRoundRawB = suppliersData.dataset.pricesListB;
const pricesPerRoundB = pricesPerRoundRawB.split(',').map(item => Number(item));
  
//Teste die gespeicherten Daten
window.onload = function() {
  console.log("round_number + 1: ", roundNumber.dataset.roundNumber + 1)
  console.log("Seite wurde geladen")
  console.log(roundNumber.dataset)
  console.log("roundsLabel: ", roundsLabel)
  console.log("suppliersDataSet: ", suppliersData.dataset)
  console.log("suppliersNumberRawA: ", suppliersData.dataset.suppliersA)
  console.log("suppliersNumberRawB: ", suppliersData.dataset.suppliersB)
  console.log("pricesPerRoundRawA: ", pricesPerRoundRawA)
  console.log("pricesPerRoundRawB: ", pricesPerRoundRawB)
  console.log("pricesPerRoundA: ", pricesPerRoundA)
  console.log("pricesPerRoundB: ", pricesPerRoundB)
  
}

//Balkendiagramm anzeigen
new Chart(ctx, {
    type: 'bar',
    data: {
      labels: roundsLabel,
      datasets: [{
        label: 'Anzahl der Verkäufer in Flohmarkt A',
        data: suppliersNumberA,
        borderWidth: 2,
        barPercentage: 0.4,
        categoryPercentage: 0.6 
    
      },{
      label: 'Anzahl der Verkäufer in Flohmarkt B',
      data: suppliersNumberB,
      borderWidth: 2,
      barPercentage: 0.4,
      categoryPercentage: 0.6}
    ]
    },
    options: {
      responsive: true,
    /*  maintainAspectRatio: false, */
      scales: {
        y: {
          beginAtZero: true
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
            const datasetIndex = context.datasetIndex; // Speichere den Index für den Datensatz in der Variable ab

            const datasetLabel = context.dataset.label;

            //Speichere die Verkäuferanzahl des aktuellen Balkens ab
            const anzahl = context.raw;

            
            const preis = datasetIndex === 0
              ? pricesPerRoundA[index]
              : pricesPerRoundB[index];

            return [
              `${datasetLabel}: ${anzahl}`,
              `Preis: ${preis} €`
            ];
          }
        }
      } 
    }
    }
});