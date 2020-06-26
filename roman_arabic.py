answerPart1 = "Please convert "
answerPart2 = 'using '
failAnswer1 = "I don't get what you want, sorry mate!"
failAnswer2 = "Hey, ask me something that's not impossible to do!"
sucAnswer = 'Sure! It is '
ascRoma = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
ascNum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
changeNum = {0: [], 1: [0], 2: [0, 0], 3: [0, 0, 0], 4: [0, 1],
             5: [1], 6: [1, 0], 7: [1, 0, 0], 8: [1, 0, 0, 0], 9: [0, 2]}
changeRom = [0, [0], [0, 0], [0, 0, 0], [0, 1], [1], [1, 0], [1, 0, 0], [1, 0, 0, 0], [0, 2]]
miniRom = {1: {'1': 1, '0': 5}, 2: {'11': 2, '01': 4, '10': 6, '12': 9}, 3: {'111': 3, '110': 7}, 4: {'1110': 8}}


def str_check(str_in):
    num_out1 = num_out2 = ''
    if answerPart1 == str_in[:len(answerPart1)]:
        str_in = str_in[len(answerPart1):]
        i = 0
        while str_in[i] != ' ':
            num_out1 += str_in[i]
            i += 1
            if i == len(str_in):
                return [1, num_out1, num_out2]
        else:
            str_in = str_in[len(num_out1) + 1:]
            if answerPart2 == str_in[:len(answerPart2)]:
                str_in = str_in[len(answerPart2):]
                i = 0
                while str_in[i] != ' ':
                    num_out2 += str_in[i]
                    i += 1
                    if i == len(str_in):
                        return [2, num_out1, num_out2]
                else:
                    return [0, num_out1, num_out2]
            elif 'minimally' == str_in:
                return [3, num_out1, num_out2]
            else:
                return [0, num_out1, num_out2]
    else:
        return [0, num_out1, num_out2]


def num_to_roman(original, asc_rom):
    if len(asc_rom) % 2:
        max_num = int(4 * (10 ** ((len(asc_rom) - 1) / 2)))
    else:
        max_num = int(9 * (10 ** (len(asc_rom) / 2 - 1)))
    if int(original) >= max_num:
        return [0]
    else:
        num_len = len(original)
        original = list(original)
        original.reverse()
        result = ''
        while num_len > 0:
            num_len -= 1
            get_roma = num_len * 2
            for j in changeNum[int(original[num_len])]:
                result += asc_rom[j + get_roma]
        return [1, result]


def roman_to_num(original, asc_rom):
    original = list(original)
    start_romania = (asc_rom.index(original[0]) // 2) * 2 + 1
    single_roman = []
    result_num = 0
    while len(original):
        if start_romania > (asc_rom.index(original[0]) // 2) * 2:
            start_romania = (asc_rom.index(original[0]) // 2) * 2
        else:
            return [0]
        for i in original:
            single_roman.append(asc_rom.index(i) - start_romania)
            if single_roman not in changeRom:
                single_roman = single_roman[:-1]
                break
        result_num += changeRom.index(single_roman) * (10 ** (start_romania // 2))
        original = original[len(single_roman):]
        single_roman.clear()
    else:
        result = str(result_num)
        return [1, result]


def restrict_roma(original):
    if original.isdigit():
        return num_to_roman(original, ascRoma)
    elif set(list(original)) | set(ascRoma) == set(ascRoma):
        return roman_to_num(original, ascRoma)
    else:
        return [0]


def general_roma(original):
    if len(set(list(original[1]))) != len(original[1]):
        return [0]
    general_list = list(original[1])
    general_list.reverse()
    if original[0].isdigit():
        return num_to_roman(original[0], general_list)
    elif original[1].isalpha() and set(list(original[0])) | set(list(original[1])) == set(list(original[1])):
        return roman_to_num(original[0], general_list)
    else:
        return [0]


def decimal_roma_generate(original):
    i_temp = 0
    dec_roma = []
    while i_temp < len(original):
        if i_temp + 2 < len(original) and original[i_temp] == original[i_temp + 2]:
            if original[i_temp] not in dec_roma:
                dec_roma.append(original[i_temp])
            if original[i_temp + 1] not in dec_roma:
                dec_roma.append(original[i_temp + 1])
        elif i_temp + 1 < len(original) and original[i_temp] == original[i_temp + 1]:
            if original[i_temp] not in dec_roma:
                dec_roma.append(original[i_temp])
        elif i_temp + 3 < len(original) and original[i_temp] == original[i_temp + 3]:
            if original[i_temp] not in dec_roma:
                dec_roma.append(original[i_temp])
            if original[i_temp + 2] not in dec_roma:
                dec_roma.append(original[i_temp + 2])
        i_temp += 1
    return dec_roma


def minimal_slice(original, dec_roma):
    original = original[::-1]
    seq_num = ''
    slice_num = 0
    slice_temp = 0
    while slice_temp < len(original):
        if not slice_num:
            slice_num = original[slice_temp]
            same_count = 1
            if slice_temp != len(original) - 1:
                slice_temp += 1
                continue
            else:
                seq_num += str(miniRom[1]['1'])  # 最高一位是单个位置的，单独处理，不在走下面流程
                break
        if original[slice_temp] == slice_num:
            same_count += 1
            if same_count > 3:
                return [0]
            if slice_temp != len(original) - 1:
                slice_temp += 1
                continue
        if slice_temp == len(original) - 1 or original[slice_temp] != slice_num:
            if same_count > 1:
                single_id = '1' * same_count
                if original[slice_temp] in dec_roma:  # check for 2 and 3
                    seq_num += str(miniRom[len(single_id)][single_id])
                    if slice_temp == len(original) - 1:
                        slice_temp += 1
                else:  # check for 7 and 8
                    single_id += '0'
                    seq_num += str(miniRom[len(single_id)][single_id])
                    slice_temp += 1
            else:
                if slice_num in dec_roma:
                    if original[slice_temp] in dec_roma:
                        if dec_roma.index(original[slice_temp]) > dec_roma.index(
                                slice_num):  # check for 9 因为两个基数之间有顺序是不能随意取值9
                            seq_num += str(miniRom[2]['12'])
                            slice_temp += 1
                        else:  # check for 1
                            seq_num += str(miniRom[1]['1'])
                    else:  # check for 6
                        seq_num += str(miniRom[2]['10'])
                        slice_temp += 1
                else:
                    if original[slice_temp] in dec_roma:
                        single_id = '01'
                        if original[slice_temp] in original[slice_temp + 1:]:
                            # if slice_temp + 1 < len(original) and slice_num == original[slice_temp]:
                            # if original[slice_temp+1]in dec_roma:
                            single_id = '1'
                            slice_temp -= 1
                        slice_temp += 1
                        seq_num += str(miniRom[len(single_id)][single_id])
                    else:  # 连续的未检测出基数的序列处理
                        unbased_num = 2
                        if slice_temp != len(original) - 1:
                            for unbased_bit in original[slice_temp + 1:]:
                                if unbased_bit not in dec_roma:
                                    unbased_num += 1
                                else:
                                    break
                        slice_temp += unbased_num - 2 + 1
                        while unbased_num > 1:
                            seq_num += str(miniRom[2]['01'])
                            unbased_num -= 2
                        if unbased_num:
                            seq_num += str(miniRom[1]['1'])
        slice_num = 0
    return seq_num[::-1]


def minimal_dict(original, mini_num):
    mini_count = 0
    start_bit = 0
    seq_list = []
    revert_bit = 0
    while mini_count < len(mini_num):
        dict_revert = int(mini_num[mini_count])
        if dict_revert is 4:
            if len(seq_list) > 0 and seq_list[-1] == ('_' or original[revert_bit + 1]):
                seq_list = seq_list[:-1]
            seq_list += [original[revert_bit + 1], original[revert_bit], '_']
            revert_bit += 2
        elif dict_revert is 9:
            if len(seq_list) > 0 and seq_list[-1] == original[revert_bit + 1]:
                seq_list = seq_list[:-1]
            elif len(seq_list) > 1 and seq_list[-2] == original[revert_bit + 1]:
                seq_list = seq_list[:-2]
            seq_list += [original[revert_bit + 1], '_', original[revert_bit], '_']
            revert_bit += 2
        elif dict_revert < 4:
            seq_list += [original[revert_bit], '_']
            revert_bit += dict_revert
        else:
            if len(seq_list) > 0 and seq_list[-1] == ('_' or original[revert_bit]):
                seq_list = seq_list[:-1]
            seq_list += [original[revert_bit], original[revert_bit + 1], '_']
            revert_bit += dict_revert - 4
        mini_count += 1
    seq_set = set(seq_list)
    seq_set.discard('_')
    if seq_list[-1] is '_':
        seq_list = seq_list[:-1]
    if len(seq_list) - seq_list.count('_') != len(seq_set):
        return [0]
    else:
        seq_rom = "".join(seq_list)
        return [2, mini_num, seq_rom]


def minimal_roma(original):
    if not original.isalpha():
        return [0]
    decimal_roma = decimal_roma_generate(original)
    if len(original) > 2:
        mini_num = minimal_slice(original, decimal_roma)
    elif len(original) is 2:
        if len(decimal_roma):
            mini_num = '2'
        else:
            mini_num = '4'
    else:
        mini_num = '1'
    if len(mini_num) > 0:
        return minimal_dict(original, mini_num)
    else:
        return [0]


def rom_convert(type_in):
    if type_in[0] == 1:  # 狭义罗马
        return restrict_roma(type_in[1])
    elif type_in[0] == 2:
        return general_roma(type_in[1:])  # 要检查输入的时候首位dict不是基数的时候，会不会正确判断溢出
    elif type_in[0] == 3:
        return minimal_roma(type_in[1])
    else:
        return [0]


feedBack = str_check(input("How can I help you? "))
if feedBack[0] == 0:
    print(failAnswer1)
elif feedBack[0] != 3 and feedBack[1][0] == '0':
    print(failAnswer1)
else:
    numBack = rom_convert(feedBack)
    if not numBack[0]:
        print(failAnswer2)
    elif numBack[0] == 1:
        print(sucAnswer + numBack[1])
    elif numBack[0] == 2:
        print(sucAnswer + numBack[1] + ' ' + answerPart2 + numBack[2])
