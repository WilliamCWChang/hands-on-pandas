import pandas
import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt

voltage_range = [4.876, 9.898, 14.822, 19.001, 24.485,
                 29.279, 34.618, 38.669, 48.112, 58.519, 68.256, 76.58, ]

tc_type_list = ["Jtype", "Ktype", "Ttype",
                "Etype", "Rtype", "Stype", "Btype", "Ntype", "78.126mV", "39.062mV", "19.532mV", ]

ohm_range = [75, 150, 240, 301, 392, 470, 560, 619,
             750, 909, 1100, 1240, 1500, 1650, 1870, 2150]

rtd_type_list = ["385", "392", "618", "672", "310", "620", "1250", "2200", ]
# rtd_type_list = ["385", "392", "618", "672"]

RTD_data = []


def readFile(filename, datasheet):
    xls_data = []
    xls = pd.ExcelFile(filename)
    for data in datasheet:
        dataframe = pd.read_excel(xls, data)[['y', 'x']]
        dataframe.columns = ['y', data]
        xls_data.append(dataframe)

    table = xls_data[0]
    for data in xls_data[1:]:
        table = pd.merge(table, data, how="outer", on='y', sort=True)

    return table.set_index("y")


def get_max_min(dataframe, datasheet, level_range):
    data_max_min_dict = {}
    # show the diff data type range
    for data_type in datasheet:
        data_max = dataframe.loc[dataframe[data_type].idxmax(), data_type]
        data_min = dataframe.loc[dataframe[data_type].idxmin(), data_type]
        data_max_min_dict.update({data_type: {}})

        for level in sorted(level_range):
            index = level_range.index(level)
            if data_max < level:
                index = index - 1
                data_max_min_dict[data_type].update({"max": index})
                break
            if level == level_range[-1]:
                if data_max >= level:
                    data_max_min_dict[data_type].update({"max": index})
            data_max_min_dict[data_type].update({"max": index})

        # print(level_range)

        for level in sorted(level_range, reverse=True):
            index = level_range.index(level)
            # print("[" + str(index) + "]" + str(data_min) + "  " + str(level))
            if data_min > level:
                index = index + 1
                data_max_min_dict[data_type].update({"min": index})
                break
            if level == level_range[-1]:
                if data_min <= level:
                    data_max_min_dict[data_type].update({"min": index})
            data_max_min_dict[data_type].update({"min": index})
    return data_max_min_dict


#############################################################
# Main
#############################################################


# TC chart
tc_df = readFile('TC_table_func.xlsx', tc_type_list)
tc_ax = tc_df.plot()
for voltage in voltage_range:
    if voltage < 20:
        tc_ax.axhline(voltage, color='r', ls="dashed")
    elif voltage < 40:
        tc_ax.axhline(voltage, color='g', ls="dashed")
    else:
        tc_ax.axhline(voltage, color='b', ls="dashed")


# # RTD chart
# rtd_ratio_list = [1, 0.5, 0.2, 0.1]
# rtd_ratio_list = [0.2]
# rtd_df = readFile('TC_table_func.xlsx', rtd_type_list)
# # rtd_df = rtd_df.reindex(index=rtd_df['y'])
# rtd_df = rtd_df.interpolate(limit_area='inside', method='values')

# for rtd_ratio in rtd_ratio_list:

#     rtd_ax = rtd_df.plot.line(title=str(rtd_ratio))
#     for ohm in ohm_range:
#         if ohm < 350:
#             rtd_ax.axhline(ohm * rtd_ratio, color='r', ls="dashed")
#         elif ohm < 700:
#             rtd_ax.axhline(ohm * rtd_ratio, color='g', ls="dashed")
#         elif ohm < 1300:
#             rtd_ax.axhline(ohm * rtd_ratio, color='pink', ls="dashed")
#         else:
#             rtd_ax.axhline(ohm * rtd_ratio, color='b', ls="dashed")


tc_max_min_dict = get_max_min(tc_df, tc_type_list, ohm_range)
for tc_type in tc_max_min_dict:
    print(tc_max_min_dict[tc_type]["max"])


# rtd_max_min_dict = get_max_min(rtd_df, rtd_type_list,
#                                [list * rtd_ratio for list in ohm_range])
# for rtd_type in rtd_max_min_dict:
#     print("type ==== " + str(rtd_max_min_dict[rtd_type]))
#     print("max = " + str(rtd_max_min_dict[rtd_type]["max"]))
#     print("min = " + str(rtd_max_min_dict[rtd_type]["min"]))


plt.show()
