from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

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
                return jsonify({"sign": sign, "fortune": f.text.strip()})
        return jsonify({"error": "띠를 찾을 수 없습니다."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()