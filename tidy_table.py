import re
import csv


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_pattern = r'(\+7|8)?[\s(-]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s)*[(]*(доб.)*[\s]*(\d+)*[\s)]*'
phone_substitute = r'+7(\2)\3-\4-\5\6\7\8'

for contact in contacts_list:
    # Приводим в порядок ФИО у каждого сотрудника: в фамилии — только фамилия,
    # в имени — только имя, в отчестве — отчество
    name_parts = ' '.join(contact[:3]).split(' ')
    contact[:3] = name_parts[:3]
    # Приводим в порядок номера телефонов по заданному образцу
    contact[5] = re.sub(phone_pattern, phone_substitute, contact[5])

# Создаём список индексов дублирующихся сотрудников
duplicate_names_indexes = []

# Ищем дубли с совпадающими фамилиями и именами и добавляем недостающие данные
# из дублей в пустые «ячейки» сотрудника, с которым сравниваем остальных
for i in range(1, len(contacts_list)):
    for j in range(i+1, len(contacts_list)):
        if contacts_list[i][:2] == contacts_list[j][:2]:
            for param in range(7):
                if contacts_list[i][param] == '':
                    contacts_list[i][param] = contacts_list[j][param]
            duplicate_names_indexes.append(j)

# Избавляемся от дублей в индексах и сортируем список по возрастанию индексов
duplicate_names_indexes = sorted(list(set(duplicate_names_indexes)))

# Удаляем дублирующихся сотрудников
counter = 1
for i in range(len(duplicate_names_indexes)):
    contacts_list.pop(duplicate_names_indexes[i])
    if i != len(duplicate_names_indexes)-1:
        duplicate_names_indexes[i+1] -= counter
        counter += 1

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
