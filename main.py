import json
import numpy as np
import redis

def split_matrix(matrix):
    # 1000×1000の行列を4つの500×500の部分行列に分割する
    matrix = np.array(matrix)
    return [
        matrix[0:500, 0:500].tolist(),
        matrix[0:500, 500:1000].tolist(),
        matrix[500:1000, 0:500].tolist(),
        matrix[500:1000, 500:1000].tolist()
    ]

def load_partial_inverses():
    # 各ワーカーの結果を読み込み、部分行列をリストに追加
    partial_inverses = []
    for i in range(1, 5):  # ワーカーIDは 1 から 4 の仮定
        with open(f'result_worker{i}.json', 'r') as f:
            partial_inverse = json.load(f)
            partial_inverses.append(partial_inverse)
    return partial_inverses

def save_final_result_to_txt(matrix):
    # 行列をテキストファイルに書き込み
    with open("inverse_matrix.txt", "w") as f:
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")

def main():
    # matrix.json から行列を読み込む
    with open("matrix.json", "r") as f:
        data = json.load(f)
        matrix = data["matrix"]

    # 行列を分割
    matrix_parts = split_matrix(matrix)

    # Redisに接続
    r = redis.Redis(host='redis', port=6379, db=0)

    # 各分割行列を Redis に保存
    for i, part in enumerate(matrix_parts):
        r.set(f"matrix_part_{i+1}", json.dumps(part))

    # 各ワーカーから収集した部分逆行列の読み込み
    partial_inverses = load_partial_inverses()

    # 行列の統合 (ここでは単純に行方向で連結する例)
    full_inverse_matrix = []
    for partial in partial_inverses:
        full_inverse_matrix.extend(partial)  # 縦方向に結合
    
    # 結果を final_result.txt に保存
    save_final_result_to_txt(full_inverse_matrix)

if __name__ == "__main__":
    main()
