main_database = []
with open('test.csv', encoding='utf-8') as f:
    for line in f:
        main_database.append(line.rstrip("\n").split(",")[0:9])
        if line[0] == '':
            break
# oldest to newest
print(len(main_database))
main_database.reverse()


def equipment_cycle_database():
    # [classification, cycles, check out times]
    equipment_cycle_usage_database = []

    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for j in range(i + 1, len(main_database)):
                # checks if same barcode and check in
                if main_database[j][2] == main_database[i][2] and main_database[j][7] == "还":
                    equipment_exist = False
                    for k in equipment_cycle_usage_database:
                        try:
                            if k[0] == f"{main_database[j][3][0].upper() + main_database[j][3][1:]}":
                                k[1] += 1
                                k[2] += ", " + main_database[i][8][0:10]
                                equipment_exist = True

                                break
                        # since some equipment name is empty
                        except IndexError:
                            if k[0] == main_database[j][3]:
                                k[1] += 1
                                k[2] += ", " + main_database[i][8][0:10]
                                equipment_exist = True
                                break
                    if not equipment_exist:
                        try:
                            equipment_cycle_usage_database.append(
                            [main_database[j][3][0].upper()+main_database[j][3][1:], 1, main_database[i][8][0:10]])
                        except IndexError:
                            equipment_cycle_usage_database.append(
                                [main_database[j][3], 1, main_database[i][8][0:10]])

                    break

    return equipment_cycle_usage_database


def user_cycle_database():
    # checks how many times a user has checked out and checked in an equipment
    # [user, type, cycles]
    user_usage_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user and barcode and check in
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    user_exist = False
                    for j in user_usage_database:
                        if j[0] == main_database[i][5]:
                            user_exist = True
                            j[2] += 1
                            break
                    if not user_exist:
                        user_usage_database.append([main_database[k][5], main_database[k][6], 1])
                    break

    return user_usage_database


def unique_user_equipment_database():
    # [equipment, [unique_users]]
    user_per_equipment_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user, barcode and checkin
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    equipment_exist = False
                    user_exist = False
                    for j in user_per_equipment_database:
                        if j[0] == main_database[k][3]:
                            equipment_exist = True
                            unique_user_list = j[1].split(', ')
                            for l in unique_user_list:
                                if l == main_database[k][5]:
                                    user_exist = True
                                    break
                            if not user_exist:
                                j[1] += ', ' + main_database[k][5]
                                break
                    if not equipment_exist:
                        user_per_equipment_database.append([main_database[k][3], main_database[k][5]])
                        break

    # [equipment, unique_users]
    user_num_equipment_database = []
    for i in range(len(user_per_equipment_database)):
        user_num_equipment_database.append([user_per_equipment_database[i][0], len(user_per_equipment_database[i][1])])
    return user_per_equipment_database


def non_unique_user_equipment_database():
    # [equipment, [non_unique_users]]
    user_per_equipment_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user, barcode and checkin
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    equipment_exist = False
                    for j in user_per_equipment_database:
                        if j[0] == main_database[k][3]:
                            equipment_exist = True
                            j[1] += ', ' + main_database[k][5]
                            break
                    if not equipment_exist:
                        user_per_equipment_database.append([main_database[k][3], main_database[k][5]])
                        break
                    break

    # [equipment, unique_users]
    user_num_equipment_database = []
    for i in range(len(user_per_equipment_database)):
        user_num_equipment_database.append([user_per_equipment_database[i][0], len(user_per_equipment_database[i][1])])
    return user_per_equipment_database


if __name__ == "__main__":
    equipment_cycle_database()
    user_cycle_database()
    unique_user_equipment_database()
    non_unique_user_equipment_database()


