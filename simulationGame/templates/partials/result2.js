<div class="modal-overlay">
  <div class="modal_header7">Ergebnisse Runde {{round_number}}</div> 
  <div class="modal-content"> 
    <div class="results-row">
      <div class="market-col1">
        <div class="market-title">Flohmarkt A</div>
        <div>Verkäufer: {{ suppliers_number_A}}  </div>
        <div>Käufer: 313</div>
        <div>Umsatz: 5839 €</div>
        <div>Käufer-Preis: 15 €</div>
        <div>Verkäufer-Preis: {{ stand_rental_A }}<span> € </span></div>
      </div>
      <div class="market-col2">
        <div class="market-title">Flohmarkt B</div>
        <div>Verkäufer: {{ suppliers_number_B }}</div>
        <div>Käufer: 246</div>
        <div>Umsatz: 5382 €</div>
        <div>Käufer-Preis: 17 €</div>
        <div>Verkäufer-Preis: {{ stand_rental_B }}<span> € </span></div>
      </div>
    </div>
    <a href=" {% if last_round %}
                 {% url 'show_winner' %}
              {% else %}
                 {% url 'round_view' nxt_round 'A' %}
              {% endif%} ">
      <button class="next-btn">
        {% if last_round  %}
          Gewinner anzeigen
        {% else %}
          weiter zur Runde {{ nxt_round }}
        {% endif %}
      </button>
    </a>
  </div>
  <div class="barChart2">
      <!-- <canvas id="myChart"></canvas> -->
      <div style="height:700px"></div>
  </div>
</div> 