def cut_res_to_output(res_value):

    more_diff_dict= {}

    for k, v in res_value.items():
    
        try:
            old_value = int(v['old_value'].replace(u'\xa0', u'').replace(' ', '').replace('р./м', '').replace('р./компл', '').replace('р./шт,600мм', '').replace('р./шт,по600мм', '').replace('р./упак(50г)', '').replace('р./кг', '').replace('руб.', ''))
            new_value = int(v['new_value'].replace(u'\xa0', u'').replace(' ', '').replace('р./м', '').replace('р./компл', '').replace('р./шт,600мм', '').replace('р./шт,по600мм', '').replace('р./упак(50г)', '').replace('р./кг', '').replace('руб.', ''))
            diff_value = new_value - old_value
            k_string = k.strip("root['()]")
            more_diff_dict[k_string] = diff_value
        except Exception as e:
            print(e)
    # так сортировать по величине значения в словаре
    diff_values_list = sorted(more_diff_dict.items(), key=lambda x: abs(x[1]))  
      
    return diff_values_list

# if __name__ == '__main__':
#     cut_res_to_output(res_value)