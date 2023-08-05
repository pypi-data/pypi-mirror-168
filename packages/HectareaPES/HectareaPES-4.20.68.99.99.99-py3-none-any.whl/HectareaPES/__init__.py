class PaneraPizza:

    def Mix(Dough, Sauce):

        for Ingredient in range(len(Dough)):

            Salt = Sauce[Ingredient%len(Sauce)]%len(Dough)
        
            Dough = PaneraPizza.Season(Ingredient, Salt, Dough)     

        return(Dough)


    def Cutter(Dough, Sauce):

        for Ingredient in range(len(Dough)-1, -1, -1):

            Salt = Sauce[Ingredient%len(Sauce)]%len(Dough)

            Dough = PaneraPizza.Season(Salt, Ingredient, Dough)     

        return(Dough)


    def Freezer(Dough, Sauce):
        for Ingredient in range(len(Dough)):
            Dough[Ingredient] = (Dough[Ingredient]+Sauce[Ingredient%len(Sauce)])%256
        return Dough


    def Oven(Dough, Sauce):
        for Ingredient in range(len(Dough)):
            Dough[Ingredient] = (Dough[Ingredient]-Sauce[Ingredient%len(Sauce)])%256
         
        return Dough


    def RollingPin(Dough, Sauce, Ingredients):
        Dough = bytearray(Dough)
        for Ingredient in range(len(Dough)):
            Dough[Ingredient] = (Dough[Ingredient]+Ingredients[Ingredient%len(Ingredients)]+Sauce[Ingredient%len(Sauce)])%256
         
        return Dough

    def Turner(Dough, Sauce,Ingredients):
        Dough = bytearray(Dough)
        for Ingredient in range(len(Dough)):
            Dough[Ingredient] = (Dough[Ingredient]-(Ingredients[Ingredient%len(Ingredients)]+Sauce[Ingredient%len(Sauce)]))%256
         
        return Dough

    def Season(Salt, Ingredient, Dough):
        Dough = bytearray(Dough)
        temp = Dough[Ingredient]
        Dough[Ingredient] = Dough[Salt]
        Dough[Salt] = temp

        return Dough