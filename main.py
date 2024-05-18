from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address
import re


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)


def login():
    try:
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print(f"ошибка авторизации: {e}")
        main()


def register():
    password = input("Введите пароль:")
    if len(password) > 12:
        if re.match(r"^[^\s]+$", password):
            if re.search('[!"#$%&\'()*+,-./:;<=>?@[\]^_{|}~]', password):
                account = w3.geth.personal.new_account(password)
                print(f"Публичный ключ: {account}")
                main()
            else:
                print("Пароль не содержит специальных символов")
        else:
            print("Пароль не должен содержать пробелов")
    else:
        print("Пароль должен быть больше 12 символов")



def createEstate(account):
    while True:
        try:
            try:
                size = int(input("Введите площадь: "))
            except ValueError:
                print("Введите число")
                continue#до сюда все гуд
            if size > 1:
                address = str(input("Введите адрес: "))
                estate_type = int(input("Выберите тип недвижимости (1 - дом, 2 - квартира, 3 - лофт): "))
                if estate_type in [1, 2, 3]:
                    tx_hash = contract.functions.createEstate(size, address, estate_type - 1).transact({
                        'from': account
                    })
                    print(f"Недвижимость {tx_hash.hex()} успешно создана")
                    break
                else:
                    print("Неверный тип недвижимости")
            else:
                print("Площадь должна быть больше 1")
        except Exception as e:
            print(f"Ошибка добавления недвижимости: {e}")

def createAd(account):
    while True:
        try:
            id = int(input("Введите id недвижимости: "))
            price = int(input("Введите цену недвижимости: "))
            tx_hash = contract.functions.createAd(id, price).transact({
                'from': account
            })
            print(f"Объявление {tx_hash.hex()} успешно создано")
            break
        except ValueError:
            print("Необходимо ввести число")
        except Exception as e:
            print(f"Ошибка добавления объявления: {e}")



def updateEstateaddress(account):
    while True:
        try:
            try:
                id = int(input("Введите id недвижимости: "))
            except ValueError:
                print("Необходимо ввести число")
                continue
            try:
                status_vybor = int(input("Выберите статус объявления\n1. Открыт\n2. Закрыт\n"))
            except ValueError:
                continue
            status = bool
            match status_vybor:
                case 1:
                    status = True
                case 2:
                    status = False
            tx_hash = contract.functions.updateEstateStatus(id, status).transact({
                'from': account,
            })
            print(f"статус был обновлен {tx_hash.hex()}")
            break
        except Exception as e:
            print(f"Ошибка обновления объявления: {e}")

def UpdateAdStatus(account):
    while True:
        try:
            while True:
                try:
                    id = int(input("Введите id объявления: "))
                except ValueError:
                    print("Необходимо ввести число")
                    continue
                tx_hash = contract.functions.updateAdStatus(id).transact({
                    'from': account,
                })
                print(f"Статус объявления изменен {tx_hash.hex()}")
                break
            break
        except Exception as e:
            print(f"Ошибка обновления статуса объявления: {e}")
            break

def BuyEstate(account):
    while True:
        try:
            while True:
                try:
                    id = int(input("Введите id объявления: "))
                    break
                except ValueError:
                    print("Это не число")
                    continue
            tx_hash = contract.functions.BuyEstate(id).transact({
                'from': account
            })
            print(f"Объявление успешно куплено {tx_hash.hex()}")
            break
        except Exception as e:
            print(f"Ошибка покупки: {e}")
            break



def get_balance(account):
    try:
        balance = contract.functions.GetBalance().call({
            "from: ": account,
        })
        print(f"Ваш баланс на смарт-контракте: {balance}")
    except Exception as e:
        print(f"Ошибка вывода баланса смарт-контракта: {e}")

def getAds(account):
    try:
        tx_hash = contract.functions.GetAds().call({
            'from': account,
        })
        print(f"объявления: {tx_hash}")
    except Exception as e:
        print(f"Ошибка вывода объявления: {e}")

def getEstates(account):
    try:
        tx_hash = contract.functions.GetEstates().call({
            'from': account,
        })
        print(f"недвижимость: {tx_hash}")
    except Exception as e:
        print(f"Ошибка вывода недвижимости: {e}")

def withdraw(account):
    try:
        while True:
            try:
                amount = int(input("Введите количество эфира для отправки:"))
                break
            except ValueError:
                print("Введите число плз")
                continue
        tx_hash = contract.functions.Withdraw(amount).transact({
            'from': account,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
    except Exception as e:
        print(f"Ошибка снятия средств: {e}")




def main():
    account = ""
    while True:
        try:
            choice = int(input("Выберите:\n1. Авторизация\n2. Регистрация\n3.Выход\n"))
        except ValueError:
            print("это не число")
            continue
        while True:
            if account == "" or account == None:
                match choice:
                    case 1:
                        account = login()
                    case 2:
                        register()
                    case 3:
                        exit()
                    case _:
                        print("Выберите 1,2 или 3")
                        break
            else:
                while True:
                    try:
                        choice = int(input("Выберите:\n1. Создать недвижимость\n2. Создать объявление\n"
                                    "3. Изменить статус недвижимости\n4. Изменить статус объявления\n"
                                    "5. Купить недвижимость\n6. Посмотреть недвижимость\n"
                                    "7. Посмотреть объявления\n8. Посмотреть баланс смарт-контракта\n"
                                    "9. Посмотреть баланс аккаунта\n10. Вывести средства\n11. Выйти\n"))
                    except ValueError:
                        print("Введите число")
                        continue
                    match choice:
                        case 1:
                            createEstate(account)
                        case 2:
                            createAd(account)
                        case 3:
                            updateEstateaddress(account)
                        case 4:
                            UpdateAdStatus(account)
                        case 5:
                            BuyEstate(account)
                        case 6:
                            getEstates(account)
                        case 7:
                            getAds(account)
                        case 8:
                            get_balance(account)
                        case 9:
                            print(f"Баланс акканута: {w3.eth.get_balance(account)}")
                        case 10:
                            withdraw(account)
                        case 11:
                            account = ""
                            main()
                        case _:
                            print("Выберите из 11 вариантов вариантов")
main()
