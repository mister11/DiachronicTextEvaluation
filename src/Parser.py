# class holds time periods for one text entry
# time periods are in format 'startYear-endYear'

from Models import TextPeriod, TextEntry

# return [TextEntry]
def parse(*file_names):
    entries = []
    for file_name in file_names:
        file = open(file_name, "r")
        text = file.read()
        text = text.replace("\n", " ")
        while True:
            index = text.find("</text>")
            if index == -1:
                break
            string_entry = text[:index]
            text = text[index + 7:]
            entries.append(__create_text_entry_from_string(string_entry))
    return entries


def __create_text_entry_from_string(string_entry):
    text_entry = TextEntry()
    text_entry.id = __get_text_entry_id(string_entry)

    # different length of time span for each text entry
    f_start = string_entry.find("textF") + 5
    f_end = string_entry.find(">", f_start)
    m_start = string_entry.find("textM") + 5
    m_end = string_entry.find(">", m_start)
    c_start = string_entry.find("textC") + 5
    c_end = string_entry.find(">", c_start)

    text_entry.textF = __get_text_entry_time_period(string_entry[f_start:f_end])
    text_entry.textC = __get_text_entry_time_period(string_entry[c_start:c_end])
    text_entry.textM = __get_text_entry_time_period(string_entry[m_start:m_end])

    text_entry.body = __get_text_entry_body(string_entry)

    return text_entry


def __get_text_entry_id(string_entry):
    start_index = string_entry.find("<text id=") + 10
    end_index = string_entry.find('\"', start_index)
    return string_entry[start_index: end_index]


def __get_text_entry_time_period(string_entry):
    text_period = TextPeriod()
    text_period.no = __get_text_entry_no_time_spans(string_entry)
    text_period.yes = __get_text_entry_yes_time_span(string_entry)
    return text_period


def __get_text_entry_yes_time_span(string_entry):
    start_index = string_entry.find("yes=") + 5
    end_index = string_entry.find('\"', start_index)
    return string_entry[start_index: end_index]


def __get_text_entry_no_time_spans(string_entry):
    time_spans = []
    while True:
        start_index = string_entry.find("no=")
        if start_index == -1:
            break
        start_index += 4
        end_index = string_entry.find('\"', start_index)
        time_spans.append(string_entry[start_index: end_index])
        string_entry = string_entry[end_index:]
    return time_spans


def __get_text_entry_body(string_entire):
    start_index = string_entire.rfind(">") + 1
    return string_entire[start_index:]