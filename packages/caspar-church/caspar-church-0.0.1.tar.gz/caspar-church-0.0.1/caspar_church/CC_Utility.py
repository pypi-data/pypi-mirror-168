#Copyright (C) <2020>  <Jeffrey Rydell>
def replace_char(String, old_character, new_character):
    List = String.split(old_character)
    new_string = List[0]
    for x in range(1,len(List)):
        new_string = new_string + new_character + List[x]
    return new_string
    
def IsNumber(String):
    try:
        x=int(String)
        return True
    except:
        return False

def checkbox_toggle(event):
    Widget = event.widget
    if Widget.value == False:
        Widget.value = True
    else:
        Widget.value = False

def fraction_to_float(string):
    num,den = string.split( '/' )
    result = (float(den)/float(num))
    return result

def find_listbox_index(Name, listbox):
    for x in range(listbox.size()):
        if str(listbox.get(x)) == Name:
            listbox.selection_set(x, x)
            listbox.active_name = Name
            listbox.see(x)
            listbox.activate(x)
            listbox.selection_set(x,x)


def List_to_CSV(List_array,divider):
    First = True
    if len(List_array) >= 0:
        for item in List_array:
            if First == True:
                CSV = str(item)
                First = False
            else:
                CSV = CSV + divider + str(item)
    return CSV

def string_to_bool(string):
    if string == "0":
        return False
    if string == "1":
        return True

def bool_to_string(Bool):
    if Bool == True:
        return "1"
    if Bool == False:
        return "0"

