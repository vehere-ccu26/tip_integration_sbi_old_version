"""
        if 'url:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/url.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'ipv4-addr:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/ipv4_addr.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'ipv6-addr:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/ipv6_addr.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'domain:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/domain.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'E-mail:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/email.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'MD5:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/md5.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        elif 'SHA1:value' in pattern_value:
            value = pattern_value.split("'")[-2]
            temp_path = PATH + '/sha1.txt'
            if check_list(temp_path,value):
                update_list(temp_path,value)
        
        else:
            pattern_status = False
        """


# curl -k -u f3ed59fa-6284-4957-897e-ad11bb1ea7de:120ef2e1-428c-4ed3-8b4e-dad8e56f84cd -H 'Accept:application/taxii+json;version=2.1' "https://tipuat.sbi.co.in/ctixapi/ctix21/collections/90a3fd96-3bd3-4ec2-a36e-37a2b766de0e/objects/"