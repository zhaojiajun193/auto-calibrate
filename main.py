from saver import Saver

dict = {
    "1":1,
    "2":2,
    "3":3
}

dict_saver = Saver()
dict_saver.save_power(dict, "./1.xlsx")

for index, key in enumerate(dict.keys()):
    print(index, key)