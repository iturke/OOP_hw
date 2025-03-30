import pickle
import shelve
import json 

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
        return self
    
class Canister(Volume):
    def __init__(self, s, f, t):
        super().__init__(s, f)  # Викликаємо конструктор батьківського класу
        self.type = t  # Тип пального
        self.octane_num = self.fuel_type()  # Зберігаємо октанове число як атрибут

    def fuel_type(self):
        """Повертає октанове число на основі типу пального."""
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

    def __eq__(self, octane_num):
        """Перевантажений оператор '==' для перевірки октанового числа."""
        if not isinstance(octane_num, int):
            raise TypeError("Октанове число має бути цілим числом")

        if self.octane_num == octane_num:
            return True
        else:
            return False


    def __str__(self):
        """Повертає рядок з інформацією про каністру."""
        return f"{super().__str__()}, Пальне: {self.type} (октанове число: {self.octane_num})"
    
    def __repr__(self):
        return f"Canister({self.size}, {self.fullness}, '{self.type}')"

class Canisters:
    def __init__(self):
        self.canisters = []  # Список для зберігання каністр

    def add_canister(self, canister):
        """Додає каністру до списку."""
        if isinstance(canister, Canister):
            self.canisters.append(canister)
        else:
            print("Це не каністра")

    def readfile(self, filename):
        """Зчитує каністри з текстового файлу та додає їх до списку."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        s = int(data[0])  # Перетворюємо size на int
                        f = int(data[1])  # Перетворюємо fullness на int
                        t = data[2]  # Тип пального
                        canister = Canister(s, f, t)
                        self.add_canister(canister)
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except Exception as e:
            print(f"Помилка при читанні файлу: {e}")

    def empty_by_octane(self, octane_num):
        """Спорожнює всі каністри з заданим октановим числом на 10%."""
        for canister in self.canisters:
            if canister.octane_num == octane_num:  # Перевіряємо октанове число
                new_fullness = canister.fullness * 0.9  # Зменшуємо заповненість на 10%
                canister.fullness = max(0, new_fullness)  # Заповненість не може бути від'ємною
                print(f"Каністра з {octane_num} октановим числом спорожнена на 10%. "
                      f"Нова заповненість: {canister.fullness} л.")
 
    def save_to_file(self, filename="canisters.pkl"): #Зберігає всі каністри у файл
        with open( filename, "wb") as file:
             pickle.dump(self.canisters, file)
        print(f" Дані збережено до файлу {filename}.")

    def load_from_file( self, filename= "canisters.pkl"): #Завантажує каністри з файлу
        with open (filename, "rb") as file:
            self.canisters = pickle.load(file)
        print(f" Дані завантажено з файлу {filename}.")    

    def save_to_shelve(self, filename="canisters.slv"):#Зберігає всі каністри у файл shelve у вигляді словника.
        with shelve.open(filename) as db:
            for canister in self.canisters:
                db[canister.type] = canister
        print(f" Дані збережено y форматі 'псевдословника' в {filename}")

    def load_from_shelve(self, filename="canisters.slv"): #Завантажує каністри з shelve у список
        self.canisters = []
        with shelve.open(filename) as db:
            for key in db:
                self.canisters.append(db[key])
        print(f"Дані завантажено з файлу {filename}")

    def save_to_text(self, filename="canisters.txt"):
        """Зберігає каністри у текстовому файлі у вигляді repr."""
        with open(filename, 'w', encoding='utf-8') as file:
            for canister in self.canisters:
                file.write(repr(canister) + '\n')
        print(f"Дані збережено у текстовому файлі {filename}")

    def load_from_text(self, filename="canisters.txt"):
        """Завантажує каністри з текстового файлу, використовуючи eval."""
        self.canisters = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                canister = eval(line.strip())
                if isinstance(canister, Canister):
                    self.add_canister(canister)
        print(f"Дані завантажено з текстового файлу {filename}")

    def save_to_json(self, filename="canisters.json"):
        """Зберігає каністри у JSON файл без зміни класу Canister."""
        data = []
        for canister in self.canisters:
            data.append({
                'size': canister.size,
                'fullness': canister.fullness,
                'type': canister.type,
                'octane_num': canister.octane_num
            })
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Дані збережено у JSON файл {filename}")

    def load_from_json(self, filename="canisters.json"):
        """Завантажує каністри з JSON файлу без зміни класу Canister."""
        self.canisters = []
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                canister = Canister(
                    s=item['size'],
                    f=item['fullness'],
                    t=item['type']
                )
                self.add_canister(canister)
        print(f"Дані завантажено з JSON файлу {filename}")


    def __str__(self):
        """Повертає рядок з інформацією про всі каністри."""
        return "\n".join(str(canister) for canister in self.canisters)
    
    def __repr__(self):#Повертає рядок, який можна використати для відтворення об'єкта.
        return f"Canisters({self.canisters})"


