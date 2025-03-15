class Volume:
    def __init__(self, s, f):
        self.size = s  
        self.fullness = min(f, s)

    def fullness_percent(self):
        return (self.fullness / self.size) * 100
    
    def __str__(self):
        return f"Місткість: {self.size} л (заповнено на {self.fullness_percent():.0f}%)"
    
    def __sub__(self, liters):
        self.fullness = max(0, self.fullness - liters)
        print(f"Ємність спорожнено на {liters} л. У ємності {self.fullness} л.")
        return Volume(self.size, max(0, self.fullness - liters))
    
class Canister(Volume): 
    def __init__(self, s, f, t):
        super().__init__(s, f)  
        self.type = t  

    def fuel_type(self):
        if self.type == "A-95":
            return 95
        elif self.type == "A-92":
            return 92
        elif self.type == "A-98":
            return 98
        elif self.type == "Дизель":
            return 0 
        else:
            raise ValueError("Невідомий тип пального")

    def __isub__(self, octane_num):
        if not isinstance(octane_num, int):
            raise TypeError("Октанове число має бути цілим числом")
        
        inp_num = self.fuel_type()
        if inp_num == octane_num:
            print(f"Октанове число пального ({inp_num}) відповідає заданому ({octane_num}).")
        else:
            print(f"Увага! Октанове число пального ({inp_num}) не відповідає заданому ({octane_num}).")
        return self

    def __str__(self):
        return f"{super().__str__()}, Пальне: {self.type} (октанове число: {self.fuel_type()})"

class Canisters 
emn = Volume(40, 16) 
o = Canister(40, 16, "A-95")
e = Canister(40, 16, "A-98")
print(o)  
print(e) 

o -= 98

 