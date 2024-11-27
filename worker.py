import json
import numpy as np
import redis
import os

def compute_inverse(matrix_part):
    # 部分行列の逆行列を計算
    return np.linalg.inv(matrix_part).tolist()

def main():
    # Redisに接続
    r = redis.Redis(host='redis', port=6379, db=0)

    # ワーカーID（例: "worker1", "worker2", ...）からインデックスを取得
    worker_id = int(os.environ["WORKER_ID"])
    matrix_part_key = f"matrix_part_{worker_id}"

    # Redisから分割行列を取得
    matrix_part = json.loads(r.get(matrix_part_key))

    # 逆行列の計算
    partial_inverse = compute_inverse(matrix_part)

    # 結果をファイルに保存
    with open(f"result_worker{worker_id}.json", "w") as f:
        json.dump(partial_inverse, f)

if __name__ == "__main__":
    main()
