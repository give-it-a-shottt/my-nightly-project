# 경로: backend/scripts/device_simulator.py
from concurrent.futures import ThreadPoolExecutor
import hashlib
import hmac
import json
import urllib.request
import urllib.error

WEBHOOK_URL = "http://localhost:8000/api/v1/webhooks/sleep"
SECRET = "device-webhook-secret-key-2026"


def send_webhook(payload: dict, custom_sig: str | None = None):
    raw_body = json.dumps(payload).encode("utf-8")
    signature = custom_sig or hmac.new(
        SECRET.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()

    req = urllib.request.Request(
        WEBHOOK_URL,
        data=raw_body,
        headers={
            "Content-Type": "application/json",
            "X-Signature": signature,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[{resp.status}] 응답:", resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[{e.code} 차단됨] 사유:", e.read().decode("utf-8"))


if __name__ == "__main__":
    sample_data = {
        "idempotency_key": "sleep_evt_20261022_001",
        "user_id": 1,  # DB의 1번 회원
        "device_serial": "SN-WATCH-001",
        "sleep_minutes": 450,
        "sleep_score": 88,
    }
    print("1) 첫 번째 정상 웹훅 전송:")
    send_webhook(sample_data)

    print("\n2) 네트워크 재시도로 똑같은 웹훅 2번째 전송:")
    send_webhook(sample_data)

    print("\n3) 해커가 가짜 서명으로 보낸 웹훅 전송:")
    send_webhook(sample_data, custom_sig="fake_hacker_signature_123")

    print("\n4) 똑같은 새 키로 동시에 20건 폭격 전송 (ThreadPoolExecutor):")
    burst_data = {
        "idempotency_key": "sleep_evt_burst_2026",
        "user_id": 1,
        "device_serial": "SN-WATCH-001",
        "sleep_minutes": 480,
        "sleep_score": 95,
    }
    with ThreadPoolExecutor(max_workers=20) as pool:
        list(pool.map(lambda _: send_webhook(burst_data), range(20)))
