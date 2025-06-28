from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import os
import json

app = Flask(__name__)

@app.route("/get_fortune", methods=["GET"])
def get_fortune():
    sign = request.args.get("sign", "쥐띠")
    url = "https://search.naver.com/search.naver?query=띠별운세"

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        signs = soup.select(".zodiac_sign .txt")
        fortunes = soup.select(".zodiac_sign .text")

        for s, f in zip(signs, fortunes):
            if sign in s.text:
                data = {"sign": sign, "fortune": f.text.strip()}
                return Response(json.dumps(data, ensure_ascii=False), mimetype="application/json")

        error = {"error": "띠를 찾을 수 없습니다."}
        return Response(json.dumps(error, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        err = {"error": str(e)}
        return Response(json.dumps(err, ensure_ascii=False), mimetype="application/json")

# 외부 접속 가능하게 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)