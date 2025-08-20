def calculate_buyer_score(request, buyer, market):
     omega = 0.63
     alpha = float(request.session["alpha"])
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
     print("buyer_willingness_to_pay: ",buyer.willingness_to_pay)
     print("entrance_fee: ", entrance_fee)
     print("pref_plce: ", pref_place)
     score = buyer.willingness_to_pay + alpha*(prev_suppliers/100) - omega*entrance_fee + pref_place
     return score