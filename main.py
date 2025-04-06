# main.py
from hwp2 import Canister, Canisters, FuelError

def main():
    try:
        # Створюємо об'єкт класу Canisters
        canisters = Canisters()

        # Додаємо каністру вручну з обробкою помилок
        try:
            canister1 = Canister(20, 15, "A-95")
            canisters.add_canister(canister1)
            print("\nПочаткові каністри:")
            print(canisters)
        except FuelError as e:
            print(f"Помилка при створенні каністри: {e}")
        except Exception as e:
            print(f"Неочікувана помилка: {e}")

        # 1. Pickle серіалізація
        print("\n1. Pickle серіалізація:")
        try:
            canisters.save_to_file()
            new_canisters = Canisters()
            new_canisters.load_from_file()
            print("Результат завантаження з pickle:")
            print(new_canisters)
        except Exception as e:
            print(f"Помилка при роботі з pickle: {e}")

        # 2. Зчитуємо каністри з текстового файлу
        print("\n2. Читання з текстового файлу:")
        try:
            canisters.readfile("kanistry.txt")
            print("Каністри після читання з kanistry.txt:")
            print(canisters)
        except Exception as e:
            print(f"Помилка при читанні з файлу: {e}")

        # 3. Shelve серіалізація
        print("\n3. Shelve серіалізація:")
        try:
            canisters.save_to_shelve()
            new_canisters1 = Canisters()
            new_canisters1.load_from_shelve()
            print("Результат завантаження з shelve:")
            print(new_canisters1)
        except Exception as e:
            print(f"Помилка при роботі з shelve: {e}")

        # 4. Текстова серіалізація (repr)
        print("\n4. Текстова серіалізація (repr):")
        try:
            canisters.save_to_text("canisters_repr.txt")
            new_canisters2 = Canisters()
            new_canisters2.load_from_text("canisters_repr.txt")
            print("Результат завантаження з текстового файлу (repr):")
            print(new_canisters2)
        except Exception as e:
            print(f"Помилка при роботі з текстовою серіалізацією: {e}")

        # 5. JSON серіалізація
        print("\n5. JSON серіалізація:")
        try:
            storage = Canisters()
            storage.add_canister(Canister(20, 15, "A-95"))
            storage.add_canister(Canister(30, 25, "A-92"))
            storage.save_to_json()
            new_storage = Canisters()
            new_storage.load_from_json()
            print("Результат завантаження з JSON:")
            print(new_storage)
        except Exception as e:
            print(f"Помилка при роботі з JSON: {e}")

        # Інші операції
        print("\nІнші операції:")
        try:
            print("Каністри перед спорожненням:")
            print(canisters)
            
            print("\nПеревірка октанового числа для каністри 1:")
            if canister1 == 65:
                print(f"Октанове число пального ({canister1.octane_num}) відповідає заданому.")
            else:
                print(f"Увага! Октанове число пального ({canister1.octane_num}) не відповідає заданому.")
            
            print("\nСпорожнення каністр з октановим числом 95 на 10%:")
            canisters.empty_by_octane(95)
            
            print("\nКаністри після спорожнення:")
            print(canisters)
        except Exception as e:
            print(f"Помилка при виконанні операцій: {e}")

    except Exception as e:
        print(f"Критична помилка: {e}")
    finally:
        print("\nПрограма завершила роботу (з помилками чи без)")

if __name__ == "__main__":
    main()