from hwp2 import Canister, Canisters  # Імпортуємо класи з файлу canister.py

def main():
    # Створюємо об'єкт класу Canisters
    canisters = Canisters()

    # Додаємо каністру вручну
    canister1 = Canister(20, 15, "A-95")
    canisters.add_canister(canister1)

    # Зчитуємо каністри з файлу
    canisters.readfile("kanistry.txt")

    # Виводимо інформацію про всі каністри перед спорожненням
    print("Каністри перед спорожненням:")
    print(canisters)
    print()

    # Перевіряємо октанове число за допомогою оператора -=
    print("Перевірка октанового числа для каністри 1:")  
    if canister1 == 65:
         print(f"Октанове число пального ({canister1.octane_num}) відповідає заданому.")
    else:
         print(f"Увага! Октанове число пального ({canister1.octane_num}) не відповідає заданому.")
   

    # Спорожнюємо каністри з октановим числом 95 на 10%
    print("Спорожнення каністр з октановим числом 95 на 10%:")
    canisters.empty_by_octane(95)
    print()

    # Виводимо інформацію про всі каністри після спорожнення
    print("Каністри після спорожнення:")
    print(canisters)

if __name__ == "__main__":
    main()