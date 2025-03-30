from hwp2 import Canister, Canisters

def main():
    # Створюємо об'єкт класу Canisters
    canisters = Canisters()

    # Додаємо каністру вручну
    canister1 = Canister(20, 15, "A-95")
    canisters.add_canister(canister1)
    print("\nПочаткові каністри:")
    print(canisters)

    # 1. Pickle серіалізація
    print("\n1. Pickle серіалізація:")
    canisters.save_to_file()
    new_canisters = Canisters()
    new_canisters.load_from_file()
    print("Результат завантаження з pickle:")
    print(new_canisters)

    # 2. Зчитуємо каністри з текстового файлу
    print("\n2. Читання з текстового файлу:")
    canisters.readfile("kanistry.txt")
    print("Каністри після читання з kanistry.txt:")
    print(canisters)

    # 3. Shelve серіалізація
    print("\n3. Shelve серіалізація:")
    canisters.save_to_shelve()
    new_canisters1 = Canisters()
    new_canisters1.load_from_shelve()
    print("Результат завантаження з shelve:")
    print(new_canisters1)

    # 4. Текстова серіалізація (repr)
    print("\n4. Текстова серіалізація (repr):")
    canisters.save_to_text("canisters_repr.txt")
    new_canisters2 = Canisters()
    new_canisters2.load_from_text("canisters_repr.txt")
    print("Результат завантаження з текстового файлу (repr):")
    print(new_canisters2)

    # 5. JSON серіалізація
    print("\n5. JSON серіалізація:")
    storage = Canisters()
    storage.add_canister(Canister(20, 15, "A-95"))
    storage.add_canister(Canister(30, 25, "A-92"))
    storage.save_to_json()
    new_storage = Canisters()
    new_storage.load_from_json()
    print("Результат завантаження з JSON:")
    print(new_storage)

    # Інші операції
    print("\nІнші операції:")
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

if __name__ == "__main__":
    main()