# hwp2.py
import pickle
import shelve
import json 

class FuelError(Exception):
    """Власний тип винятку для помилок, пов'язаних з паливом."""
    pass

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
        try:
            assert s > 0, "Розмір каністри має бути більше 0"
            assert f >= 0, "Заповненість не може бути від'ємною"
            super().__init__(s, f)  # Викликаємо конструктор батьківського класу
            self.type = t  # Тип пального
            self.octane_num = self.fuel_type()  # Зберігаємо октанове число як атрибут
        except AssertionError as e:
            raise FuelError(f"Невірні параметри каністри: {e}")
        except Exception as e:
            raise FuelError(f"Помилка при створенні каністри: {e}")

    def fuel_type(self):
        """Повертає октанове число на основі типу пального."""
        try:
            if self.type == "A-95":
                return 95
            elif self.type == "A-92":
                return 92
            elif self.type == "A-98":
                return 98
            elif self.type == "Дизель":
                return 0
            else:
                raise FuelError(f"Невідомий тип пального: {self.type}")
        except FuelError as e:
            raise e
        except Exception as e:
            raise FuelError(f"Помилка при визначенні типу пального: {e}")

    def __eq__(self, octane_num):
        """Перевантажений оператор '==' для перевірки октанового числа."""
        try:
            if not isinstance(octane_num, int):
                raise TypeError("Октанове число має бути цілим числом")
            return self.octane_num == octane_num
        except Exception as e:
            raise FuelError(f"Помилка при перевірці октанового числа: {e}")

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
        try:
            if isinstance(canister, Canister):
                self.canisters.append(canister)
            else:
                raise FuelError("Спроба додати об'єкт, який не є каністрою")
        except FuelError as e:
            print(f"Помилка: {e}")

    def readfile(self, filename):
        """Зчитує каністри з текстового файлу та додає їх до списку."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        data = line.strip().split(',')
                        if len(data) == 3:
                            s = int(data[0])
                            f = int(data[1])
                            t = data[2]
                            canister = Canister(s, f, t)
                            self.add_canister(canister)
                    except ValueError as e:
                        print(f"Помилка при перетворенні даних у рядку '{line}': {e}")
                    except FuelError as e:
                        print(f"Помилка при створенні каністри з рядка '{line}': {e}")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except Exception as e:
            print(f"Неочікувана помилка при читанні файлу {filename}: {e}")

    def empty_by_octane(self, octane_num):
        """Спорожнює всі каністри з заданим октановим числом на 10%."""
        try:
            assert isinstance(octane_num, int), "Октанове число має бути цілим числом"
            for canister in self.canisters:
                try:
                    if canister.octane_num == octane_num:
                        new_fullness = canister.fullness * 0.9
                        canister.fullness = max(0, new_fullness)
                        print(f"Каністра з {octane_num} октановим числом спорожнена на 10%. Нова заповненість: {canister.fullness} л.")
                except Exception as e:
                    print(f"Помилка при спорожненні каністри: {e}")
        except AssertionError as e:
            print(f"Невірний параметр: {e}")
        except Exception as e:
            print(f"Неочікувана помилка при спорожненні каністр: {e}")
 
    def save_to_file(self, filename="canisters.pkl"):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.canisters, file)
            print(f"Дані збережено до файлу {filename}.")
        except Exception as e:
            print(f"Помилка при збереженні у pickle: {e}")

    def load_from_file(self, filename="canisters.pkl"):
        try:
            with open(filename, "rb") as file:
                self.canisters = pickle.load(file)
            print(f"Дані завантажено з файлу {filename}.")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except Exception as e:
            print(f"Помилка при завантаженні з pickle: {e}")

    def save_to_shelve(self, filename="canisters.slv"):
        try:
            with shelve.open(filename) as db:
                for canister in self.canisters:
                    db[canister.type] = canister
            print(f"Дані збережено у форматі 'псевдословника' в {filename}")
        except Exception as e:
            print(f"Помилка при збереженні у shelve: {e}")

    def load_from_shelve(self, filename="canisters.slv"):
        try:
            self.canisters = []
            with shelve.open(filename) as db:
                for key in db:
                    self.canisters.append(db[key])
            print(f"Дані завантажено з файлу {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except Exception as e:
            print(f"Помилка при завантаженні з shelve: {e}")

    def save_to_text(self, filename="canisters.txt"):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for canister in self.canisters:
                    file.write(repr(canister) + '\n')
            print(f"Дані збережено у текстовому файлі {filename}")
        except Exception as e:
            print(f"Помилка при збереженні у текстовий файл: {e}")

    def load_from_text(self, filename="canisters.txt"):
        try:
            self.canisters = []
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        canister = eval(line.strip())
                        if isinstance(canister, Canister):
                            self.add_canister(canister)
                    except Exception as e:
                        print(f"Помилка при обробці рядка '{line.strip()}': {e}")
            print(f"Дані завантажено з текстового файлу {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except Exception as e:
            print(f"Помилка при завантаженні з текстового файлу: {e}")

    def save_to_json(self, filename="canisters.json"):
        try:
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
        except Exception as e:
            print(f"Помилка при збереженні у JSON: {e}")

    def load_from_json(self, filename="canisters.json"):
        try:
            self.canisters = []
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    try:
                        canister = Canister(
                            s=item['size'],
                            f=item['fullness'],
                            t=item['type']
                        )
                        self.add_canister(canister)
                    except KeyError as e:
                        print(f"Відсутнє обов'язкове поле у JSON: {e}")
                    except FuelError as e:
                        print(f"Помилка при створенні каністри з JSON: {e}")
            print(f"Дані завантажено з JSON файлу {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except json.JSONDecodeError:
            print(f"Файл {filename} містить некоректний JSON.")
        except Exception as e:
            print(f"Помилка при завантаженні з JSON: {e}")

    def __str__(self):
        return "\n".join(str(canister) for canister in self.canisters)
    
    def __repr__(self):
        return f"Canisters({self.canisters})"