from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import translation
from django.utils.translation import gettext as _
from .models import Supplier, Buyer
import random
import numpy as np


def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)

# Create your views here.
def welcome(request):
       request.session.flush()  
       return render(request, 'welcome.html', {})
def configuration(request):
        error = ""
        if request.method == "GET":
          request.session.flush()
          request.session["configured"] = False
          request.session[f'buyers_numberA_in_round_0'] = 500
          request.session[f'buyers_numberB_in_round_0'] = 500
          request.session[f'suppliers_numberA_in_round_0'] = 50
          request.session[f'suppliers_numberB_in_round_0'] = 50
        if request.method == "POST": 
            game_rounds_number = request.POST.get("game_rounds_number")
            cross_side = request.POST.get("cross_side")
            # Prüfen ob beide Felder ausgefüllt sind
            if game_rounds_number and cross_side:
            # Werte speichern (z.B. in Session)
              request.session["game_rounds_number"] = game_rounds_number
              request.session["cross_side"] = cross_side
              if cross_side == "option_1":
                   request.session["beta"] = 20
                   request.session["alpha"] = 50
              elif cross_side == "option_2":
                   request.session["beta"] = 50
                   request.session["alpha"] = 20
              else:
                   request.session["beta"] = 30
                   request.session["alpha"] = 30
              request.session["configured"] = True
          #    print("alpha: ", request.session.get("alpha"))
          #    print("beta: ", request.session.get("beta"))
              # Redirect zu round page
              return redirect('round_view', round_number=1, market='A')
            else:
               error = "Bitte wähle beide Optionen aus."
               return render(request, "configuration_site.html", {"error": error})
        return render(request, 'configuration_site.html', {"error": error})


def round_view(request, round_number, market):
    
    if request.session.get("configured") == False or round_number > int(request.session.get("game_rounds_number")):
         return redirect("configuration")
    if request.method == "POST":
        # Werte aus dem Formular holen
        if market == 'A':
           # print("POST-Bedingung erfüllt!")
            eintritt_A = request.POST.get('eintritt')
            stand_rental_A = request.POST.get('standmiete')
 
            # In der Session speichern
            request.session["stand_rental_A"] = stand_rental_A
            request.session["entrance_fee_A"] = eintritt_A
            request.session[f'entrance_fee_A_in_round_{round_number}'] = eintritt_A
            request.session[f'stand_rental_A_in_round_{round_number}'] = stand_rental_A
            
            # Beispiel: Markt wechseln
            market = 'B' 
            return redirect('round_view', round_number, market)
        if market == 'B':
          #  print("POST-Bedingung erfüllt!")
            eintritt_B = request.POST.get('eintritt')
            stand_rental_B = request.POST.get('standmiete')
 
            # In der Session Preise speichern
            request.session["stand_rental_B"] = stand_rental_B
            request.session["entrance_fee_B"] = eintritt_B
            request.session[f'entrance_fee_B_in_round_{round_number}'] = eintritt_B
            request.session[f'stand_rental_B_in_round_{round_number}'] = stand_rental_B
            
            # ToDo rufe eine View auf für die Berechnung der neuen Anzahl an Käufer und Verkäufer
            suppliers_number_A, suppliers_number_B = calculate_suppliers_number(request)
            buyers_number_A, buyers_number_B = calculate_buyers_number(request)
            #berechne die Umsätze:
            stand_rental_A = int(request.session["stand_rental_A"])
            eintritt_A = int(request.session["entrance_fee_A"])
            stand_rental_B = int(stand_rental_B)
            eintritt_B = int(eintritt_B)
            UmsatzA = suppliers_number_A*stand_rental_A + buyers_number_A*eintritt_A
            UmsatzB = suppliers_number_B*stand_rental_B + buyers_number_B*eintritt_B 
            request.session[f'UmsatzA_in_round_{round_number}'] = UmsatzA
            request.session[f'UmsatzB_in_round_{round_number}'] = UmsatzB
          #  print("buyers_number_A: ", buyers_number_A)
          #  print("buyers_number_B: ", buyers_number_B) 
           # speichere die Anzahl der Käufer und Verkäufer
            request.session[f'suppliers_numberA_in_round_{round_number}'] = suppliers_number_A
            request.session[f'suppliers_numberB_in_round_{round_number}'] = suppliers_number_B
            request.session[f'buyers_numberA_in_round_{round_number}'] = buyers_number_A
            request.session[f'buyers_numberB_in_round_{round_number}'] = buyers_number_B
            return redirect('results', round_number)
            # return redirect('results', suppliers_number_A, suppliers_number_B, buyers_number_A, buyers_number_B)
    
    return render(request, 'round_site.html', {
        'round': round_number,
        'market': market,
    })

def results_view(request, round_number):
     #In der Session den Anteil in der letzten Runde speichern
     request.session['prev_buyers_A'] = request.session.get(f'buyers_numberA_in_round_{round_number - 1}')
     request.session['prev_buyers_B'] = request.session.get(f'buyers_numberB_in_round_{round_number - 1}')
     request.session['prev_suppliers_A'] = request.session.get(f'suppliers_numberA_in_round_{round_number - 1}')
     request.session['prev_suppliers_B'] = request.session.get(f'suppliers_numberB_in_round_{round_number - 1}')
     last_round = False
     if round_number is None:
        return HttpResponse("Fehler: Rundenanzahl nicht in der Session vorhanden.", status=400)
     stand_rental_A = request.session["stand_rental_A"]
     stand_rental_B = request.session["stand_rental_B"]
     entrance_fee_A = request.session["entrance_fee_A"]
     entrance_fee_B = request.session["entrance_fee_B"]
     buyers_number_A = request.session[f'buyers_numberA_in_round_{round_number}']
     buyers_number_B = request.session[f'buyers_numberB_in_round_{round_number}']
     suppliers_number_A = request.session[f'suppliers_numberA_in_round_{round_number}']
     suppliers_number_B = request.session[f'suppliers_numberB_in_round_{round_number}']
     UmsatzA = request.session.get(f'UmsatzA_in_round_{round_number}')
     UmsatzB = request.session.get(f'UmsatzB_in_round_{round_number}')
     if round_number == int(request.session['game_rounds_number']):
     #     print(f"Rundenanzahl: {round_number} sind fertig abgelaufen")
          last_round = True
     nxt_round = round_number + 1
     # Speichere die Verkäuferanzahl sowie die gesetzte Preise von Flohmärkten A und B in Listen 
     suppliers_number_list_A = []
     suppliers_number_list_B = []
     buyers_number_list_A = []
     buyers_number_list_B = []
     supplier_prices_list_A = []
     supplier_prices_list_B = []
     buyer_prices_list_A = []
     buyer_prices_list_B = []
     Umsatz_list_A = []
     Umsatz_list_B = []
     for i in range(1, round_number + 1):

          # supplier daten speicheren 
          varA = request.session.get(f'suppliers_numberA_in_round_{i}')
          varB = request.session.get(f'suppliers_numberB_in_round_{i}')
          varC = request.session.get(f'stand_rental_A_in_round_{i}')
          varD = request.session.get(f'stand_rental_B_in_round_{i}')

          # buyers daten speichern
          varA2 = request.session.get(f'buyers_numberA_in_round_{i}')
          varB2 = request.session.get(f'buyers_numberB_in_round_{i}')
          varC2 = request.session.get(f'entrance_fee_A_in_round_{i}')
          varD2 = request.session.get(f'entrance_fee_B_in_round_{i}')
                                      
          #Umsätze speicher
          varA3 = request.session.get(f'UmsatzA_in_round_{i}')
          varB3 = request.session.get(f'UmsatzB_in_round_{i}')
                                      
         # supplier listen mit den Daten befüllen                           
          suppliers_number_list_A.append(varA)
          suppliers_number_list_B.append(varB)
          supplier_prices_list_A.append(varC)
          supplier_prices_list_B.append(varD)

         # buyer listen mit den Daten befüllen                           
          buyers_number_list_A.append(varA2)
          buyers_number_list_B.append(varB2)
          buyer_prices_list_A.append(varC2)
          buyer_prices_list_B.append(varD2)

          # Umsätze in Listen umfüllen
          Umsatz_list_A.append(varA3)
          Umsatz_list_B.append(varB3)

  #   print("buyers_number_list_A: ", buyers_number_list_A)
  #   print("buyers_number_list_B: ", buyers_number_list_B)
  #   print("buyer_prices_list_A: ", buyer_prices_list_A)
  #   print("supplier_prices_list_A: ", supplier_prices_list_A)
  #   print("supplier_prices_list_B: ", supplier_prices_list_B)
  #   print("buyer_prices_list_A: ", supplier_prices_list_A)
  #   print("stand_Rental_A: ", stand_rental_A)
  #   print("stand_Rental_B: ", stand_rental_B)
     context = {
        'round_number': round_number,
        'nxt_round': nxt_round,
        'last_round': last_round,
        'suppliers_number_A': suppliers_number_A,
        'suppliers_number_B': suppliers_number_B,
        'buyers_number_A': buyers_number_A,
        'buyers_number_B': buyers_number_B,
        'stand_rental_A': stand_rental_A,
        'stand_rental_B': stand_rental_B,
        'entrance_fee_A': entrance_fee_A,
        'entrance_fee_B': entrance_fee_B,
        'UmsatzA': UmsatzA,
        'UmsatzB': UmsatzB,
        'suppliers_number_list_A': suppliers_number_list_A,
        'suppliers_number_list_B': suppliers_number_list_B,
        'supplier_prices_list_A': supplier_prices_list_A,
        'supplier_prices_list_B': supplier_prices_list_B,
        'buyers_number_list_A': buyers_number_list_A, 
        'buyers_number_list_B': buyers_number_list_B, 
        'buyer_prices_list_A': buyer_prices_list_A,
        'buyer_prices_list_B': buyer_prices_list_B,
        'Umsatz_list_A': Umsatz_list_A,
        'Umsatz_list_B': Umsatz_list_B
    }
     request.session["Umsatz_list_A"] = Umsatz_list_A
   #  print(f'Umsatz_list_A: {request.session.get("Umsatz_list_A")}')
    # for element in request.session.get("Umsatz_list_A"):
       #   print(element, "->", type(element))
     request.session["Umsatz_list_B"] = Umsatz_list_B
     return render(request, 'results_site.html', context)


def test(request):
       return render(request, 'test.html', {})   


def calculate_suppliers_number(request):
    suppliers_list = Supplier.objects.all()
    list_suppliersA = []
    list_suppliersB = []
    j = 0
    for supplier in suppliers_list:     
         supplier.travel_cost_to_A = random.randint(5,100)
         supplier.travel_cost_to_B = random.randint(5,100)

         if j == 20:
            #   print("supplier: ", {j})
               pass
         #      break
       #  print("supplier:", {j+1})
         j = j +1
         scoreA_supplier = calculate_supplier_score(request, supplier, market= "A") 
     #    print("scoreA_supplier: ", scoreA_supplier)
         scoreB_supplier = calculate_supplier_score(request, supplier, market = "B")
     #    print("scoreB_supplier: ", scoreB_supplier)
     #    print("scoreA - scoreB: ", scoreA_supplier - scoreB_supplier)

      #   print("****************")
         if scoreA_supplier <= 0 and scoreB_supplier <= 0:
              continue
         if scoreA_supplier > scoreB_supplier:
               list_suppliersA.append(supplier)
         elif scoreA_supplier < scoreB_supplier:
               list_suppliersB.append(supplier)
         else:
              if supplier.preference == "A":
                   list_suppliersA.append(supplier)
              else:
                   list_suppliersB.append(supplier)
  #  print("list_suppliersA_length: ", len(list_suppliersA))
  #  print("list_suppliersB_length: ",  len(list_suppliersB))
  #   arr = np.array(su)
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
  #  print("willingness_to_pay: ", supplier.willingness_to_pay )
  #  print("gamma*stand_rental: ", gamma*stand_rental)
  #  print("stand_rental: ", stand_rental)
  #  print("prev_buyers: ", prev_buyers)
    score = supplier.willingness_to_pay + beta*(prev_buyers/1000) -  gamma*stand_rental - 0.2*travel_cost
    return score

def calculate_buyers_number(request):
     buyers_list = Buyer.objects.all()
     list_buyersA = []
     list_buyersB = []
     i = 0
     for buyer in buyers_list:
          if i == 10 :
               pass
             #  break
       #   print("buyer: ", {i+1}) 
          scoreA_buyer = round(calculate_buyer_score(request, buyer, market= "A"), 2)
       #   print("scoreA: ", scoreA_buyer)
          scoreB_buyer = round(calculate_buyer_score(request, buyer, market= "B"), 2) 
      #    print("scoreB: ", scoreB_buyer)
      #    print("************")
          i = i+1
          if scoreA_buyer <= 0 and scoreB_buyer <= 0:
               continue
          if scoreA_buyer > scoreB_buyer:
               list_buyersA.append(buyer)
          elif scoreA_buyer < scoreB_buyer:
               list_buyersB.append(buyer)
          else:
              if buyer.preference == "A":
                   list_buyersA.append(buyer)
              else:
                   list_buyersB.append(buyer)
      #    print(f"list_buyrsA: {len(list_buyersA)}")
      #    print(f"list_buyrsB: {len(list_buyersB)}")
     return len(list_buyersA), len(list_buyersB)

def winner_view(request):
     Umsatz_list_A = request.session.get("Umsatz_list_A")
   #  print("Umsatz_list_A: ", Umsatz_list_A)
     sum_A = sum(Umsatz_list_A)
     Umsatz_list_B = request.session.get("Umsatz_list_B")
     sum_B = sum(Umsatz_list_B)
     winner = 'A' if sum_A > sum_B else 'B'
     if sum_A == sum_B:
          return render(request, 'draw_site.html', {'sum_A':sum_A})
     return render(request, 'winner_site.html', {'sum_A':sum_A, 'sum_B':sum_B, 'winner': winner})
      
     
def calculate_buyer_score(request, buyer, market):
     omega = 0.8
     alpha = float(request.session["alpha"])
     """
         if buyer.out_door_pf == 0:
          print("out_door")
          pref_place = buyer.in_door_pf
       else:
          print("in_door")
          pref_place = buyer.out_door_pf 
     """
     if market == "A":       
           prev_suppliers = int(request.session["prev_suppliers_A"])
           entrance_fee = int(request.session["entrance_fee_A"])
   #        print("entrance_feeA: ", entrance_fee)
           pref_place = buyer.out_door_pf
     else:
          prev_suppliers = int(request.session["prev_suppliers_B"])
          entrance_fee = int(request.session["entrance_fee_B"])
    #      print("entrance_feeB: ", entrance_fee)
          pref_place = buyer.in_door_pf
    # print("buyer_willingness_to_pay: ",buyer.willingness_to_pay)
    # print("entrance_fee: ", entrance_fee)
    # print("pref_plce: ", pref_place)
     score = buyer.willingness_to_pay + alpha*(prev_suppliers/100) - omega*entrance_fee  +  pref_place 
 #    print("buyer_willingness_to_pay: ",buyer.willingness_to_pay)
 #    print("entrance_fee: ", omega*entrance_fee)
   #  print("entrance_fee: ", entrance_fee)
  #   print("buyer.out_door_pf: ", buyer.out_door_pf)
  #   print("buyer.in_door_pf: ", buyer.in_door_pf)
  #   print("pref_place: ", pref_place)
  #   print("score: ", score)
    # score = pref_place 
     return score

def draw_view(request):
     return render(request, 'draw_site.html', {})
def instructions_view(request):
     return render(request, 'explanation_site.html', {})












