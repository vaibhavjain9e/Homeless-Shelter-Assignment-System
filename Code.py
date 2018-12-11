class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class Applicant:
    def __init__(self, applicant_id, gender, age, pets, medical_conditions, car, dl, days, lahsa, spla, week, value):
        self.applicant_id = applicant_id
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medical_conditions = medical_conditions
        self.car = car
        self.dl = dl
        self.days = days
        self.lahsa = lahsa
        self.spla = spla
        self.week = week
        self.value = value


unique_efficiency_list = []
sorted_efficiency_list = []
common_id_value_list = []
common_id_sorted_list = []
add_all_days_value = False
answer_found = False
file = open('input.txt', 'r')
input_list = file.read().split('\n')

bed_count = int(input_list[0])  # b <= 40
spaces_parking_lot_count = int(input_list[1])
LAHSA_applicants_count = int(input_list[2])

LAHSA_applicants_list = []
SPLA_applicants_list = []
applicants_list = []

LAHSA_applicants_start_index = 3
LAHSA_applicants_end_index = LAHSA_applicants_start_index + LAHSA_applicants_count - 1
for item in input_list[LAHSA_applicants_start_index: LAHSA_applicants_end_index + 1]:
    LAHSA_applicants_list.append(int(item))

SPLA_applicants_count = int(input_list[LAHSA_applicants_end_index + 1])
SPLA_applicants_start_index = LAHSA_applicants_end_index + 2
SPLA_applicants_end_index = SPLA_applicants_start_index + SPLA_applicants_count - 1

for item in input_list[SPLA_applicants_start_index: SPLA_applicants_end_index + 1]:
    SPLA_applicants_list.append(int(item))

applicants_count = int(input_list[SPLA_applicants_end_index + 1])

applicants_start_index = SPLA_applicants_end_index + 2
applicants_end_index = applicants_start_index + applicants_count - 1

for item in input_list[applicants_start_index: applicants_end_index + 1]:
    applicants_list.append(item)

week_lahsa = [bed_count] * 7
week_spla = [spaces_parking_lot_count] * 7
all_applicants = []
applicant_dict = {}

for item in applicants_list:
    weeks = item[13:20]
    value = int(weeks[0]) + int(weeks[1]) + int(weeks[2]) + int(weeks[3]) + int(weeks[4]) + int(weeks[5]) + int(
        weeks[6])
    week_per_applicant = [int(weeks[0]), int(weeks[1]), int(weeks[2]), int(weeks[3]), int(weeks[4]),
                          int(weeks[5]), int(weeks[6])]
    all_applicants.append(Applicant(int(item[0:5]), item[5], int(item[6:9]), item[9], item[10], item[11], item[12],
                                    item[7], False, False, week_per_applicant, value))

    applicant_dict[int(item[0:5])] = week_per_applicant


lahsa_final_list = []
spla_final_list = []

for app_id in SPLA_applicants_list:
    for i in range(len(all_applicants)):
        if app_id == all_applicants[i].applicant_id:
            week_spla[0] -= all_applicants[i].week[0]
            week_spla[1] -= all_applicants[i].week[1]
            week_spla[2] -= all_applicants[i].week[2]
            week_spla[3] -= all_applicants[i].week[3]
            week_spla[4] -= all_applicants[i].week[4]
            week_spla[5] -= all_applicants[i].week[5]
            week_spla[6] -= all_applicants[i].week[6]
            del all_applicants[i]
            break

for app_id in LAHSA_applicants_list:
    for i in range(len(all_applicants)):
        if app_id == all_applicants[i].applicant_id:
            week_lahsa[0] -= all_applicants[i].week[0]
            week_lahsa[1] -= all_applicants[i].week[1]
            week_lahsa[2] -= all_applicants[i].week[2]
            week_lahsa[3] -= all_applicants[i].week[3]
            week_lahsa[4] -= all_applicants[i].week[4]
            week_lahsa[5] -= all_applicants[i].week[5]
            week_lahsa[6] -= all_applicants[i].week[6]
            del all_applicants[i]
            break

spla_applicants = []
lahsa_applicants = []
common_applicants = []


def segregate_applicants():
    exists_in_lahsa = False
    exists_in_spla = False
    for applicant in all_applicants:
        if applicant.gender == 'F' and applicant.age > 17 and applicant.pets == 'N':
            applicant.lahsa = True
            exists_in_lahsa = True
        if applicant.car == 'Y' and applicant.dl == 'Y' and applicant.medical_conditions == 'N':
            applicant.spla = True
            exists_in_spla = True
        if exists_in_lahsa and exists_in_spla:
            common_applicants.append(applicant)
            lahsa_applicants.append(applicant)
            spla_applicants.append(applicant)
            exists_in_spla = False
            exists_in_lahsa = False
        if exists_in_lahsa and not exists_in_spla:
            lahsa_applicants.append(applicant)
            exists_in_spla = False
            exists_in_lahsa = False
        if exists_in_spla and not exists_in_lahsa:
            spla_applicants.append(applicant)
            exists_in_spla = False
            exists_in_lahsa = False


segregate_applicants()

common_comparison_list = common_applicants[:]
spla_comparison_list = spla_applicants[:]
lahsa_comparsison_list = lahsa_applicants[:]

for element in common_applicants:
    common_id_value_list.append((element.applicant_id, element.value))

common_id_value_list.sort(key=lambda x: (-x[1], x[0]))

for cid in common_id_value_list:
    common_id_sorted_list.append(cid[0])


temp_week_spla = week_spla[:]
temp_spla_applicants = spla_applicants[:]
temp_spla_common_list = []
temp_spla_list = []
answer = 0


class State:
    def __init__(self, spla_assigned_pool, spla_remaining_pool, lahsa_assigned_pool, lahsa_remaining_pool, week_spla, week_lahsa):
        self.spla_assigned_pool = spla_assigned_pool
        self.spla_remaining_pool = spla_remaining_pool
        self.lahsa_assigned_pool = lahsa_assigned_pool
        self.lahsa_remaining_pool = lahsa_remaining_pool
        self.week_spla = week_spla
        self.week_lahsa = week_lahsa

    def __str__(self):
        return ''.join(map(str, self.spla_assigned_pool)) + ''.join(map(str, self.lahsa_assigned_pool)) + ''.join(map(str, self.spla_remaining_pool)) + ''.join(map(str, self.lahsa_remaining_pool))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.spla_assigned_pool == other.spla_assigned_pool and self.lahsa_assigned_pool == other.lahsa_assigned_pool and self.lahsa_assigned_pool == other.lahsa_assigned_pool and self.lahsa_remaining_pool == other.lahsa_remaining_pool


def do_iterative_deepening_search(week_spla, week_lahsa):
    global answer

    lahsa_assigned_pool = []
    spla_assigned_pool = []
    spla_remaining_pool = []
    lahsa_remaining_pool = []

    for applicant in lahsa_applicants:
        lahsa_remaining_pool.append(applicant.applicant_id)

    for applicant in spla_applicants:
        spla_remaining_pool.append(applicant.applicant_id)

    stack = Stack()

    stack.push(State(spla_assigned_pool, spla_remaining_pool, lahsa_assigned_pool, lahsa_remaining_pool, week_spla, week_lahsa))

    negative_element_found = False
    combination_list = set()
    data_store = set()

    while stack.size() > 0:
        element = stack.pop()
        spla_remaining_pool = element.spla_remaining_pool
        spla_assigned_pool = element.spla_assigned_pool
        lahsa_remaining_pool = element.lahsa_remaining_pool
        lahsa_assigned_pool = element.lahsa_assigned_pool
        week_spla = element.week_spla
        week_lahsa = element.week_lahsa

        if len(spla_remaining_pool) == 0 and len(lahsa_remaining_pool) == 0:
            element.spla_assigned_pool = set(spla_assigned_pool)
            element.lahsa_assigned_pool = set(lahsa_assigned_pool)
            combination_list.add(element)

        if len(spla_remaining_pool) == 0 and len(lahsa_remaining_pool) > 0:
            for j in range(len(lahsa_remaining_pool)):
                z = lahsa_assigned_pool[:]
                z.append(lahsa_remaining_pool[j])

                m = lahsa_remaining_pool[0:j] + lahsa_remaining_pool[j + 1:len(lahsa_remaining_pool)]

                check_week_lahsa = week_lahsa[:]
                for c in range(len(check_week_lahsa)):
                    check_week_lahsa[c] -= applicant_dict[lahsa_remaining_pool[j]][c]
                    if check_week_lahsa[c] < 0:
                        lahsa_return = lahsa_remaining_pool[:]
                        del lahsa_return[j]

                        vv = set(spla_assigned_pool)
                        mm = set(lahsa_assigned_pool)
                        aa = set(spla_remaining_pool)
                        bb = set(lahsa_return)
                        state_object = State(vv, aa, mm, bb, week_spla, week_lahsa)
                        if state_object not in data_store:
                            data_store.add(state_object)
                            stack.push(State(spla_assigned_pool, spla_remaining_pool, lahsa_assigned_pool, lahsa_return,
                                    week_spla, week_lahsa))
                        negative_element_found = True
                        break

                if negative_element_found:
                    negative_element_found = False
                    continue

                vv = set(spla_assigned_pool)
                mm = set(z)
                aa = set(spla_remaining_pool)
                bb = set(m)
                state_object = State(vv, aa, mm, bb, week_spla, check_week_lahsa)
                if state_object not in data_store:
                    data_store.add(state_object)
                    stack.push(State(spla_assigned_pool, spla_remaining_pool, z, m, week_spla, check_week_lahsa))

        elif len(spla_remaining_pool) > 0:
            for i in range(len(spla_remaining_pool)):
                y = spla_assigned_pool[:]
                y.append(spla_remaining_pool[i])
                n2 = spla_remaining_pool[0:i] + spla_remaining_pool[i + 1:len(spla_remaining_pool)]

                check_week_spla = week_spla[:]
                for c in range(len(check_week_spla)):
                    check_week_spla[c] -= applicant_dict[spla_remaining_pool[i]][c]

                    if check_week_spla[c] < 0:
                        spla_return = spla_remaining_pool[:]
                        del spla_return[i]

                        vv = set(spla_assigned_pool)
                        mm = set(lahsa_assigned_pool)
                        aa = set(spla_return)
                        bb = set(lahsa_remaining_pool)
                        state_object = State(vv, aa, mm, bb, week_spla,week_lahsa)
                        if state_object not in data_store:
                            data_store.add(state_object)
                            stack.push(State(spla_assigned_pool, spla_return, lahsa_assigned_pool, lahsa_remaining_pool, week_spla, week_lahsa))
                        negative_element_found = True
                        break

                if negative_element_found:
                    negative_element_found = False
                    continue

                new_lahsa_remaining_pool = lahsa_remaining_pool[:]
                if spla_remaining_pool[i] in new_lahsa_remaining_pool:
                    new_lahsa_remaining_pool.remove(spla_remaining_pool[i])

                if len(new_lahsa_remaining_pool) > 0:
                    for j in range(len(new_lahsa_remaining_pool)):
                        z = lahsa_assigned_pool[:]
                        z.append(new_lahsa_remaining_pool[j])

                        m = new_lahsa_remaining_pool[0:j] + new_lahsa_remaining_pool[
                                                            j + 1:len(new_lahsa_remaining_pool)]
                        n = spla_remaining_pool[0:i] + spla_remaining_pool[i + 1:len(spla_remaining_pool)]
                        for item in z:
                            if item in n:
                                n.remove(item)

                        check_week_lahsa = week_lahsa[:]
                        for c in range(len(check_week_lahsa)):
                            check_week_lahsa[c] -= applicant_dict[new_lahsa_remaining_pool[j]][c]
                            if check_week_lahsa[c] < 0:
                                lahsa_return = new_lahsa_remaining_pool[:]
                                del lahsa_return[j]
                                vv = set(y)
                                mm = set(lahsa_assigned_pool)
                                aa = set(n)
                                bb = set(lahsa_return)
                                state_object = State(vv, aa, mm, bb, check_week_spla, week_lahsa)
                                if state_object not in data_store:
                                    data_store.add(state_object)
                                    stack.push(State(y, n, lahsa_assigned_pool, lahsa_return,
                                            check_week_spla, week_lahsa))
                                negative_element_found = True
                                break

                        if negative_element_found:
                            negative_element_found = False
                            continue

                        vv = set(y)
                        mm = set(z)
                        aa = set(n)
                        bb = set(m)
                        state_object = State(vv, aa, mm, bb, check_week_spla, check_week_lahsa)
                        if state_object not in data_store:
                            data_store.add(state_object)
                            stack.push(State(y, n, z, m, check_week_spla, check_week_lahsa))
                else:
                    vv = set(y)
                    mm = set(lahsa_assigned_pool)
                    aa = set(n2)
                    bb = set(new_lahsa_remaining_pool)
                    state_object = State(vv, aa, mm, bb, check_week_spla, week_lahsa)
                    if state_object not in data_store:
                        data_store.add(state_object)
                        stack.push(State(y, n2, lahsa_assigned_pool, new_lahsa_remaining_pool, check_week_spla, week_lahsa))

    efficiency_list = []
    for item1 in combination_list:
        efficiency_list.append((list(item1.spla_assigned_pool), sum(item1.week_spla), list(item1.lahsa_assigned_pool), sum(item1.week_lahsa)))

    global unique_efficiency_list

    for item1 in efficiency_list:
        if item1 not in unique_efficiency_list:
            unique_efficiency_list.append(item1)



do_iterative_deepening_search(week_spla, week_lahsa)


def lahsa_sorting(lahsa_list):
    new_lahsa_list = []
    for la in lahsa_list:
        new_lahsa_list.append((la, sum(applicant_dict[la])))

    temp_id_list = []
    new_lahsa_list.sort(key=lambda x: (-x[1], x[0]))

    for ele in new_lahsa_list:
        temp_id_list.append(ele[0])

    lahsa_list = temp_id_list

    index1 = 0
    for j in range(0, len(lahsa_list)):
        if lahsa_list[j]in common_id_sorted_list:
            temp = lahsa_list[j]
            lahsa_list[j] = lahsa_list[index1]
            lahsa_list[index1] = temp
            index1 += 1

    return lahsa_list


def spla_sorting(spla_list):
    new_spla_list = []
    for sp in spla_list:
        new_spla_list.append((sp, sum(applicant_dict[sp])))

    temp_id_list = []
    new_spla_list.sort(key=lambda x: (-x[1], x[0]))

    for ele in new_spla_list:
        temp_id_list.append(ele[0])

    spla_list = temp_id_list

    index1 = 0
    for j in range(0, len(spla_list)):
        if spla_list[j] in common_id_sorted_list:
            temp = spla_list[j]
            spla_list[j] = spla_list[index1]
            spla_list[index1] = temp
            index1 += 1

    return spla_list


if answer == 0:
    for item in unique_efficiency_list:
        s = spla_sorting(item[0])
        l = lahsa_sorting(item[2])
        sorted_efficiency_list.append((s, item[1], l, item[3]))

    sorted_efficiency_list.sort(key=lambda x: (x[1], x[3], x[0]))

    temp_list = []

    for sss in sorted_efficiency_list:
        temp_list.append((sss[0], sss[2]))

    sorted_efficiency_list = temp_list[:]

    go_to_next_element = False

    try:
        for element in sorted_efficiency_list:
            index = 0
            common_list = common_id_sorted_list[:]

            if len(element[1]) > 0:
                while index <= len(element[0]) - 1 and index <= len(element[1]) - 1:
                    lahsa_value = element[1][index]
                    spla_value = element[0][index]
                    lahsa_efficiency = sum(applicant_dict[lahsa_value])
                    spla_sublist = element[0][0:index + 1]
                    lahsa_sublist = element[1][0: index + 1]
                    if lahsa_value in common_list and spla_value in common_list:
                        for element2 in sorted_efficiency_list:
                            if len(element2[0]) > index:
                                if element2[0][0:index + 1] == spla_sublist:
                                    if len(element2[1]) > index:
                                        if sum(applicant_dict[element2[1][index]]) > lahsa_efficiency:
                                            go_to_next_element = True
                                            break

                    else:
                        answer_found = True
                        answer = element[0][0]
                        break

                    if go_to_next_element:
                        go_to_next_element = False
                        break
                    else:
                        index += 1
                        if index > len(element[0]) - 1 or index > len(element[1]) - 1:
                            answer_found = True
                            answer = element[0][0]
                            break

                if answer_found:
                    break
            else:
                answer_found = True
                answer = element[0][0]
                break

    except:
        if len(sorted_efficiency_list) > 0:
            answer = sorted_efficiency_list[0][0][0]

if not add_all_days_value and not answer_found:
    if len(sorted_efficiency_list) > 0:
        answer = sorted_efficiency_list[0][0][0]

string_answer = str(answer)
while len(string_answer) < 5:
    string_answer = '0' + string_answer

with open('output.txt', 'w') as outputFile:
    outputFile.write(string_answer)
