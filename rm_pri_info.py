import re

#시
def filtering_si(address):
    result = []

    p = re.compile('[가-힣]{2,6}시\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        if len(tmp_result) > 5:
            result.append(tmp_result[:2])
        else:
            result.append(tmp_result[:-2])
 
    return result


#도
def filtering_do(address):
    result = []

    p = re.compile('[가-힣]{2,6}도\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        if len(tmp_result) == 5:
            result.append(tmp_result[:3:2])
            result.append(tmp_result[:2])
    
    return result


#구
def filtering_gu(address):
    result = []

    p = re.compile('[가-힣]{1,4}구\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        if len(tmp_result) == 3:
            result.append(tmp_result[:-1])
        else:
            result.append(tmp_result[:-2])
    
    return result


#군
def filtering_gun(address):
    result = []

    p = re.compile('[가-힣]{2}군\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        result.append(tmp_result[:-2])
    
    return result


# 읍
def filtering_eup(address):
    result = []

    p = re.compile('[가-힣]{2,3}읍\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        result.append(tmp_result[:-2])

    return result


# 면
def filtering_myeon(address):
    result = []

    p = re.compile('[가-힣]{1,5}면\s')
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        result.append(tmp_result[:-2])

    return result


# 동, 리
def filtering_dong_ri(address):
    result = []

    p = re.compile('[가-힣0-9\.]{1,5}[동리][\s\,\)]') # 도로명 주소의 경우 맨 뒤 괄호안에 들어가는 경우도 있기 때문에 ,와)를 넣음
    fi_result = p.findall(address)

    for tmp_result in fi_result:
        # 2글자일 경우
        if len(tmp_result) == 3:
            result.append(tmp_result[:2])
        else:
            i = 0
            while True:
                if tmp_result[i].isdigit(): 
                    # 중간에 숫자가 들어간 경우
                    result.append(tmp_result[:i])
                    break
                else:
                    # 숫자가 안들어간 경우
                    if i == len(tmp_result) - 3:
                        result.append(tmp_result[:-2])
                        break    
                i = i + 1

    return result


# 가
def filtering_ga(address):
    result = []

    p = re.compile('[가-힣]{1,4}[동로][0-9]가[\s\,\)]')
    fi_result = p.findall(address)
    
    for tmp_result in fi_result:
        # 4글자일 경우
        if len(tmp_result) == 5:
            result.append(tmp_result[:-3])
        else:
            result.append(tmp_result[:-4])

    return result


# 로~길
def filtering_ro1(address):
    result = []

    p = re.compile('[가-힣0-9]{1,6}[^동서남북][동서남북대]로[\s0-9]') # 3,4글자면 '로' 전만 살려, 숫자 나오면 그 전 부분만 살려, 모두 아니면 '*로' 전만 살려 
    fi_result = p.findall(address)
    
    for tmp_result in fi_result:
        # 3,4글자일 경우
        if len(tmp_result) <= 5:
            result.append(tmp_result[:2])
        else:
            i = 0
            while True:
                if tmp_result[i].isdigit(): 
                    # 마지막에 숫자가 들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-3])
                        break
                    # 중간에 숫자가 들어간 경우
                    else: 
                        result.append(tmp_result[:-i])
                        break
                else:
                    # 숫자가 안들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-3])
                        break    
                i = i + 1 

    return result


def filtering_ro2(address):
    result = []

    p = re.compile('([가-힣0-9]{1,6}[동서남북]{2,}[0-9]*로[\s0-9])|([가-힣0-9]{1,6}중앙[0-9]*로[\s0-9])')
    fi_result = p.findall(address)
    if fi_result:
        fi_result = list(fi_result[0])
        fi_result = ' '.join(fi_result).split()
    else:
        fi_result = []

    for tmp_result in fi_result:
        # 4,5글자일 경우
        if len(tmp_result) <= 6:
            result.append(tmp_result[:2]) 
        else:
            i = 0
            while True:
                if tmp_result[i].isdigit(): 
                    # 마지막에 숫자가 들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-4])
                        break
                    # 중간에 숫자가 들어간 경우
                    else: 
                        result.append(tmp_result[:i-2])
                        break
                else:
                    # 숫자가 안들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-3])
                        break    
                i = i + 1 

    return result


def filtering_ro3(address):
    result = []
    p = re.compile('[가-힣A-Za-z0-9\.]{1,6}[^동서남북대]로[\s0-9가나다라마바사아자차카타]') # 위와 비슷하게(아래와 같음)
    fi_result = p.findall(address)
    
    for tmp_result in fi_result:
        # 3글자일 경우
        if len(tmp_result) == 4:
            result.append(tmp_result[:2])
        else:
            i = 0
            while True:
                if tmp_result[i].isdigit(): 
                    # 마지막에 숫자가 들어간 경우
                    if i == len(tmp_result) - 1: 
                        result.append(tmp_result[:-3])
                        break
                    # 중간에 숫자가 들어간 경우
                    else: 
                        result.append(tmp_result[:i])
                        break
                else:
                    # 숫자가 안들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-2])
                        break    
                i = i + 1 

    return result


def filtering_gil(address):
    result = []

    p = re.compile('[가-힣0-9]{1,7}길[\s0-9]')
    fi_result = p.findall(address)
    
    for tmp_result in fi_result:
        # 3글자일 경우
        if len(tmp_result) == 4:
            result.append(tmp_result[:2])
        else:
            i = 0
            while True:
                if tmp_result[i].isdigit(): 
                    # 마지막에 숫자가 들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-3])
                        break
                    # 중간에 숫자가 들어간 경우
                    else:
                        result.append(tmp_result[:i])
                        break
                else:
                    # 숫자가 안들어간 경우
                    if i == len(tmp_result) - 1:
                        result.append(tmp_result[:-2])
                        break    
                i = i + 1 

    return result


def filtering_ro_gil(address):
    result = []

    p = re.compile('[가-힣0-9]{1,5}로[가-힣]{2,}길\s')
    fi_result = p.findall(address)
    
    # 뒤에서부터 '로'를 찾으면 '로'이후부터 '길'이전까지
    for tmp_result in fi_result:
        i = -4
        while True:
            if '로' == tmp_result[i]:
                result.append(tmp_result[i+1:-2])
                break
            else:
                i = i - 1
    
    return result


def filtering_address(address):
    result = filtering_si(address) + filtering_do(address) + filtering_gu(address) \
        + filtering_gun(address) + filtering_eup(address) + filtering_myeon(address) \
        + filtering_dong_ri(address) + filtering_ga(address)

    if filtering_ro1(address) or filtering_ro2(address) or filtering_ro3(address):
        tmp_list = []

        if filtering_ro1(address):
            len_ro1 = len(filtering_ro1(address)[0])
        else:
            len_ro1 = 20

        if filtering_ro2(address):
            len_ro2 = len(filtering_ro2(address)[0])
        else:
            len_ro2 = 20

        if filtering_ro3(address):
            len_ro3 = len(filtering_ro3(address)[0])
        else:
            len_ro3 = 20

        tmp_list.append(len_ro1)
        tmp_list.append(len_ro2)
        tmp_list.append(len_ro3)

        if tmp_list.index(min(tmp_list)) == 0:
            result = result + filtering_ro1(address)
        elif tmp_list.index(min(tmp_list)) == 1:
            result = result + filtering_ro2(address)
        else:
            result = result + filtering_ro3(address)

    else:
        tmp_list = []

        if filtering_gil(address):
            len_gil = len(filtering_gil(address)[0])
        else:
            len_gil = 20

        if filtering_ro_gil(address):
            len_ro_gil = len(filtering_ro_gil(address)[0])
        else:
            len_ro_gil = 20

        tmp_list.append(len_gil)
        tmp_list.append(len_ro_gil)

        if tmp_list.index(min(tmp_list)) == 0:
            result = result + filtering_gil(address)
        else:
            result = result + filtering_ro_gil(address)
    
    result = set(result)
    return list(result)


# -------------------------------- 주소 -------------------------------------


def filtering_sex1(sex, tag):
    # 태그가 1 글자 일경우
    if sex == '남자':
        result = ['남', '男']
    else:
        result = ['여', '녀', '女']

    for res in result:
        if tag[0] == res:
            return True

    return False


def filtering_sex2(sex, tag): 
    # 태그가 2글자 이상의 문자열일 때 비교
    if sex == '남자':
        result = ['남자', '男']
    else:
        result = ['여자', '女']

    for res in result:
        if res in tag:
            return True

    return False


# -------------------------------- 성별 -------------------------------------


def filtering_name(name):
    result = []
    result.append(name[-2:])

    return result


# -------------------------------- 이름 -------------------------------------


from datetime import datetime
def filtering_age(birth):
    result = []

    age = datetime.today().year - int(birth[:4]) + 1 # 실제 나이
    result.append(str(age))

    now = str(datetime.today().month) + str(datetime.today().day) # 현재 날짜
    man_chk = int(now) - int(birth[4:]) # 생일이 지났는지, 안지났는지

    if man_chk >= 0:
        man_age = '만' + str(age - 1)
        result.append(man_age)
    else:
        man_age = '만' + str(age - 2)
        result.append(man_age)

    return result


# -------------------------------- 나이 -------------------------------------

from flask import flash
import pybo.views.auth_views

def Delete_SA_Data(user_id, tag):

    conn, cursor = pybo.views.auth_views.create_connection()
    sql = "select name, sex, age, address from users where id=%s"
    cursor.execute(sql, user_id)

    check_validate = cursor.fetchall() 
    if len(check_validate) == 0: 
        flash("존재하지 않는 사용자입니다.")
        return [] 
    else: 
        private_info = list(check_validate[0])
        hash_tag = tag

    #ex)
    #"충청북도 청주시 사운로359번길 13"
    #"서울특별시 마포구 가양대로 117(상암동)"
    #"세종특별자치시 연동면 한누리대로 1168"
    #"경상남도 서울특별시 마산합포구 군위군 조치원읍 그대라면 송림3.5동 필동2가 올림픽대로 가장산업서북로 대학로5번길 몰이산길 명지국제4로가길 경복대로가마솥골길 20"

    result = []

    # 성별만 비교 후 삭제
    i = 0
    while True:
        if len(hash_tag[i]) == 1:
            if filtering_sex1(private_info[1], hash_tag[i]):
                del hash_tag[i]
                i = i - 1
        else:
            if filtering_sex2(private_info[1], hash_tag[i]):
                del hash_tag[i]
                i = i - 1
        if len(hash_tag) - 1 == i:
            break
        i = i + 1

    # 성별를 제외한 나머지 개인정보 핵심 단어 모으기 
    result = filtering_name(private_info[0]) + filtering_age(private_info[2]) + filtering_address(private_info[3])

    # 비교 후 포함하는 태그 삭제
    for res in result:
        i = 0
        while True:
            if res in hash_tag[i]:
                del hash_tag[i]
                i = i - 1
            if len(hash_tag) - 1 == i:
                break
            i = i + 1

    return hash_tag