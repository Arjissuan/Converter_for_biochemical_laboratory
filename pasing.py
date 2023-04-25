import pandas
import os

def parse_sachoza(droga,plik, gdzie, nazwa):
    data = pandas.DataFrame( columns=("stężenie", "temperatura", "data", "godzina"))
    st = []
    jd_st = []
    tmp = []
    jd_tmp = []
    dt = []
    hr = []
    with open("{}\\{}".format(droga,plik), "r") as my_file:
        for record in my_file.readlines():
            rec = record.split(" ")
            rec[:] = (value for value in rec if value != "")
            st.append(rec[1].replace(",", "."))
            jd_st.append(rec[2])
            tmp.append(rec[3].replace(',', '.'))
            jd_tmp.append(rec[4])
            dt.append(rec[len(rec) - 2])
            hr.append(rec[len(rec) - 1].split("\n")[0])
        data["stężenie"] = st
        data["jednostka_stężenia"]  =jd_st
        data["temperatura"] = tmp
        data["jednostka_tempreratury"] = jd_tmp
        data["data"] = dt
        data["godzina"] = hr
        print(data)
        return data.to_excel(f"{gdzie}\\{nazwa}.xlsx", engine="xlsxwriter")


def parsing(path, name, where_path, new_name):
    data = pandas.DataFrame()
    with open(os.path.join(path, name)) as my_file:
        content = my_file.readlines()
        line_len = content[0].split(" ")
        line_len[:] = (value for value in line_len if value != "")
        for cols in range(len(line_len)):
            column = []
            for record in content:
                rec = record.split(" ")
                rec[:] = (value for value in rec if value != "")
                rec[cols] = rec[cols].replace("\n", " ")
                column.append(rec[cols].replace(",", "."))
            data[f"{cols}"] = column
    return data.to_excel(os.path.join(where_path, f"{new_name}.xlsx"), engine="xlsxwriter")
