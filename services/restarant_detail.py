from flask import Flask, render_template
from restarant import app  # 여기에는 Flask 애플리케이션의 인스턴스가 들어가야 합니다.
from restarant import Restarants  # Restaurants 모델이 정의된 파일 또는 모듈의 경로로 수정

@app.route('/restarant/<int:restarant_id>', methods=['GET'])
def restarant_detail(restarant_id):
    # restarant_id에 해당하는 레스토랑 정보를 데이터베이스에서 가져와서 상세 페이지에 전달
    restarant = Restarants.query.get_or_404(restarant_id)
    return render_template('restarant_detail.html', restarant=restarant)

if __name__ == '__main__':
    app.run(debug=True)

