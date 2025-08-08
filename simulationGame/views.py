from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Supplier, Buyer
import random


# Create your views here.
def welcome(request):
       return render(request, 'welcome.html', {})
def configuration(request):
        """
        if request.session.get("round_number"):
            del request.session["round_number"] 
        """
        request.session.clear()
        error = ""
        request.session["configured"] = False
        request.session["prev_buyers_A"] = 0.5
        request.session["prev_buyers_B"] = 0.5
        request.session["prev_suppliers_A"] = 0.5
        request.session["prev_suppliers_A"] = 0.5
        if request.method == "POST": 
            game_rounds_number = request.POST.get("game_rounds_number")
            cross_side = request.POST.get("cross_side")
            # Prüfen ob beide Felder ausgefüllt sind
            if game_rounds_number and cross_side:
            # Werte speichern (z.B. in Session)
              request.session["game_rounds_number"] = game_rounds_number
              request.session["cross_side"] = cross_side
              if cross_side == "option_1":
                   request.session["beta"] = 15
                   request.session["alpha"] = 3
              elif cross_side == "option_2":
                   request.session["beta"] = 3
                   request.session["alpha"] = 15
              else:
                   request.session["beta"] = 10
                   request.session["alpha"] = 10
              request.session["configured"] = True
              # Redirect zu round page
              return redirect('round_view', round_number=1, market='A')
            else:
               error = "Bitte wähle beide Optionen aus."
               return render(request, "configuration_site.html", {"error": error})
        return render(request, 'configuration_site.html', {"error": error})


def round_view(request, round_number, market):
    if request.session.get("configured") == False or round_number > int(request.session.get("game_rounds_number")):
         return redirect("configuration")
#    if request.session.get("rundenanzahl"):
 #        if n > int(request.session.get("rundenanzahl")):
  #            return redirect("configuration")

  # speichere die aktuell Rundennummer in der Session
    request.session['round_number'] = round_number
    if request.method == "POST":
        # Werte aus dem Formular holen
        if market == 'A':
           # print("POST-Bedingung erfüllt!")
            eintritt_A = request.POST.get('eintritt')
            stand_rental_A = request.POST.get('standmiete')
 
            # In der Session speichern
            request.session["stand_rental_A"] = stand_rental_A
            request.session[f'eintritt_A_in_Runde_{round_number}'] = eintritt_A
            request.session[f'stand_rental_A_in_Runde_{round_number}'] = stand_rental_A
            
            # Beispiel: Markt wechseln
            market = 'B' 
        #  request.session['runde'] = runde */
          #  request.session['markt'] = markt 
            print("Market: " + market)
        # Seite neu rendern 
            return redirect('round_view', round_number, market)
        if market == 'B':
            print("POST-Bedingung erfüllt!")
            eintritt_B = request.POST.get('eintritt')
            stand_rental_B = request.POST.get('standmiete')
 
            # In der Session speichern
            request.session["stand_rental_B"] = stand_rental_B
            request.session[f'eintritt_B_in_Runde_{round_number}'] = eintritt_B
            request.session[f'stand_rental_B_in_Runde_{round_number}'] = stand_rental_B
            calculate_suppliers_number(request)
            # ToDo rufe eine View auf für die Berechnung der neuen Anzahl an Käufer und Verkäufer
            suppliers_number_A, suppliers_number_B = calculate_suppliers_number(request)
          #  buyers_number_A, buyers_number_B = calculate_buyers_number(request) 
            request.session[f'suppliers_numberA_in_round_{round_number}'] = suppliers_number_A
            request.session[f'suppliers_numberB_in_round_{round_number}'] = suppliers_number_B
            return redirect('results', suppliers_number_A, suppliers_number_B)

    
    return render(request, 'round_site.html', {
        'runde': round_number,
        'market': market,
    })

def results_view(request, suppliers_number_A, suppliers_number_B):
     
     last_round = False
     round_number = request.session.get("round_number")
     if round_number is None:
        return HttpResponse("Fehler: Rundenanzahl nicht in der Session vorhanden.", status=400)
     stand_rental_A = request.session["stand_rental_A"]
     stand_rental_B = request.session["stand_rental_B"]
     if round_number == int(request.session['game_rounds_number']):
          print(f"Rundenanzahl: {round_number} sind fertig abgelaufen")
          last_round = True
     nxt_round = round_number + 1
     # Speichere die Verkäuferanzahl sowie die gesetzte Preise von Flohmärkten A und B in Listen 
     suppliers_number_list_A = []
     suppliers_number_list_B = []
     prices_list_A = []
     prices_list_B = []
     for i in range(1, round_number + 1):
          varA = request.session.get(f'suppliers_numberA_in_round_{i}')
          varB = request.session.get(f'suppliers_numberB_in_round_{i}')
          varC = request.session.get(f'stand_rental_A_in_Runde_{i}')
          varD = request.session.get(f'stand_rental_B_in_Runde_{i}')
          suppliers_number_list_A.append(varA)
          suppliers_number_list_B.append(varB)
          prices_list_A.append(varC)
          prices_list_B.append(varD)
     print("prices_list_A: ",prices_list_A)
     print("prices_list_B: ",prices_list_B)
     print("stand_Rental_A: ", stand_rental_A)
     print("stand_Rental_B: ", stand_rental_B)
     context = {
        'round_number': round_number,
        'nxt_round': nxt_round,
        'last_round': last_round,
        'suppliers_number_A': suppliers_number_A,
        'suppliers_number_B': suppliers_number_B,
        'stand_rental_A': stand_rental_A,
        'stand_rental_B': stand_rental_B,
        'suppliers_number_list_A': suppliers_number_list_A,
        'suppliers_number_list_B': suppliers_number_list_B,
        'prices_list_A': prices_list_A,
        'prices_list_B': prices_list_B 
    }
     return render(request, 'results_site.html', context)


def test(request):
       return render(request, 'test.html', {})   
def calculate_suppliers_number(request):
    suppliers_list = Supplier.objects.all()
    """
    prev_buyers_A = request.session["prev_buyers_A"]
    prev_buyers_B = request.session["prev_buyers_B"]
    stand_rental_A = request.session["standmiete_A"] 
    stand_rental_B = request.session["standmiete_B"]  
    beta = request.session.get("beta")
    """

    list_suppliersA = []
    list_suppliersB = []
    for supplier in suppliers_list:     
         supplier.travel_cost_to_A = random.uniform(5,40)
         supplier.travel_cost_to_B = random.uniform(5,40)
         scoreA_supplier = calculate_supplier_score(request, supplier, market= "A") 
         scoreB_supplier = calculate_supplier_score(request, supplier, market = "B")
         if scoreA_supplier > scoreB_supplier:
               list_suppliersA.append(supplier)
         elif scoreA_supplier < scoreB_supplier:
               list_suppliersB.append(supplier)
         else:
              if supplier.preference == "A":
                   list_suppliersA.append(supplier)
              else:
                   list_suppliersB.append(supplier)
    print("list_suppliersA_length: ", len(list_suppliersA))
    print("list_suppliersB_length: ",  len(list_suppliersB))
    return len(list_suppliersA), len(list_suppliersB)

def calculate_supplier_score(request, supplier, market):
    gamma = 0.2
    beta = float(request.session["beta"])
    if market == "A":
         prev_buyers = int(request.session["prev_buyers_A"])
         travel_cost = supplier.travel_cost_to_A
         stand_rental = int(request.session["stand_rental_A"])

    else: # if market == "B"
        prev_buyers = int(request.session["prev_buyers_B"])
        travel_cost = supplier.travel_cost_to_B
        stand_rental = int(request.session["stand_rental_B"])
         
    score = supplier.willingness_to_pay + beta*(prev_buyers/1000) - gamma*stand_rental - travel_cost
    return score

def calculate_buyers_number(request):
     buyers_list = Buyer.object.all()
     list_suppliersA = []
     list_suppliersB = []
     for buyer in buyers_list:
          scoreA = calculate_buyer_score(request, buyer, market= "A")
          scoreB = calculate_buyer_score(request, buyer, market= "B") 
          
          
          




def winner_view(request):
     return HttpResponse("<h1>Der Gewinner ist Flohmarkt A</h1>")
     

