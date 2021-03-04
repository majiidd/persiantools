from persiantools.digits import fa_to_en

third_digit = {
    "1": "صد",
    "2": "دویست",
    "3": "سیصد",
    "4": "چهارصد",
    "5": "پانصد",
    "6": "ششصد",
    "7": "هفتصد",
    "8": "هشتصد",
    "9": "نهصد",
}

second_digit_one = {
    "0": "ده",
    "1": "یازده",
    "2": "دوازده",
    "3": "سیزده",
    "4": "چهارده",
    "5": "پانزده",
    "6": "شانزده",
    "7": "هفده",
    "8": "هجده",
    "9": "نوزده",
}

second_digit = {
    "0": "",
    "2": "بیست",
    "3": "سی",
    "4": "چهل",
    "5": "پنجاه",
    "6": "شصت",
    "7": "هفتاد",
    "8": "هشتاد",
    "9": "نود",
}

first_digit = {
    "0": "",
    "1": "یک",
    "2": "دو",
    "3": "سه",
    "4": "چهار",
    "5": "پنج",
    "6": "شش",
    "7": "هفت",
    "8": "هشت",
    "9": "نه",
}

ordes = {
    0: '',
    1: 'هزار',
    2: 'میلیون',
    3: 'میلیارد',
    4: 'تریلیون',
}



def three_digit_def(digits):
    result_string = ""
    digits = fa_to_en(digits)
    if len(digits)==3:
        if digits[1]=="1":
            result_string += (third_digit[digits[0]] + ' و ' + second_digit_one[digits[2]])
        else:
            result_string += third_digit[digits[0]]
            if digits[1] != '0':
                result_string += (' و ' + second_digit[digits[1]])
            if digits[2] != '0':
                result_string += (' و ' + first_digit[digits[2]])
    elif len(digits)==2:
        if digits[0]=="1":
            result_string += second_digit_one[digits[1]]
        else:
            result_string += second_digit[digits[0]]
            if digits[1]!="0":
                result_string += (' و ' + first_digit[digits[1]])
    elif len(digits)==1:
        if digits[0]=="0":
            result_string = 'صفر'
        else:
            result_string+= (first_digit[digits[0]])

    return result_string

def number_to_leter(number):
    number = str(number)
    digits =[number[0:len(number)%3]] + [number[i:i+3] for i in range(len(number)%3, len(number), 3)]

    if '' in digits:
        digits.remove('')

    my_str = ""
    i = len(digits)
    for item in digits:

        if item!='000':
            item = str(int(item))
            if i!=1:
                my_str += (three_digit_def(item) + ' ' + ordes[i-1] + ' و ')
            else:
                my_str += (three_digit_def(item) + ' ' + ordes[i-1])

        i-=1
    if my_str[-1:-4:-1]==' و ':
        my_str = my_str[:-3]

    return my_str