from flask import Flask, flash, render_template, request, Blueprint, url_for
from werkzeug.utils import secure_filename
from werkzeug.utils import redirect
from flask import session
from pybo import db
from pymongo import MongoClient

## 사용자 함수 정의
from rm_pri_info import Delete_SA_Data # 민감정보 처리
from recommend_hash import recommender # 해시태그 추천
from detect_face_parts import Deid_Img # 이미지 비식별

import datetime

bp = Blueprint('upload', __name__, url_prefix='/upload')

# 업로드 HTML 렌더링
@bp.route('/upload')
def render_file():
    return render_template('upload/upload.html')

@bp.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        pic = request.files['pic']        
        values = request.form.getlist("value") # 사용자 입력 해시태그
        user_id = session.get('user_id')       # 세션에 저장된 유저 아이디
        img_name = pic.filename                # image name ex) test.jpg
        
        print('user id : ', user_id)
        pic.save("user_image/" + secure_filename(img_name))

        try:
            try:
                filtered_hash = Delete_SA_Data(user_id, values) # 민강정보 처리
            except:
                print('filter error')
            try:
                recommend_hashtag_list = recommender(img_name)  # 해시태그 추천
            except:
                print('recommend hash error')
            try:
                upload_result = Deid_Img("user_image/" + img_name) # 이미지 비식별
            except:
                print('deid img error')

            if upload_result:
                # 해시태그 제거
                search = '#'
                for i, word in enumerate(recommend_hashtag_list):
                    if search in word:
                        recommend_hashtag_list[i] = word.strip(search)

                all_hash = list(set(values + recommend_hashtag_list)) # 해시태그 합치기 
                print(all_hash)
                
                Save_In_DB(user_id, img_name, all_hash) # mongoDB에 저장

            else:
                pass

        except:
            print("Error")
            pass
    
        # s3 경로랑 url 반환하는 메소드
        # return redirect(url_for('auth.login'))
        return redirect(url_for('upload.render_file'))


def Save_In_DB(user_id, img_name, all_hash):
    # mongoDB Insert Data
    try:
        client = MongoClient('',) # ubuntu
        db = client.mybide # DB 연결
        print('DB connected')
    except:
        print('connect failed')

    now = datetime.datetime.now()

    confirm_id = db.images.find_one({"_id": user_id}) # 처음 업로드 하는지 확인
    if not confirm_id:
        image_info = {
        "_id" : user_id,
        "id" : user_id # fix - it
        }
        db.images.insert_one(image_info)
        print('insert success')

    else:
        print('id is already exsist')
        pass

    metatag = {
        "image_path" : img_name,
        "created_at" : now.strftime('%Y-%m-%d'),
        'tag' : all_hash
    }
    
    try:
        db.images.update_one({"_id":user_id}, {'$push':{"image":metatag}}) # update_one(조건문, 수정내용)
        print('update success')
    except:
        print('update Failed')
