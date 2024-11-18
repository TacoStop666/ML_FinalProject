import pandas as pd

# 檔案名稱
input_file = "processed_output.csv"  # 請將這裡替換為你的 CSV 文件名稱

def count_hashtags(input_file):
    """
    計算 CSV 文件中 `hashtag` 欄位內的 `#` 總數。
    """
    # 讀取 CSV 文件
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"讀取 CSV 文件時出錯：{e}")
        return
    
    # 確保存在 `hashtag` 欄位
    if 'hashtag' not in df.columns:
        print("CSV 文件中找不到 `hashtag` 欄位！")
        return
    
    # 計算每行的 `#` 數量
    def count_hashes_in_row(row):
        if isinstance(row, str):  # 確保是字串
            return row.count('#')
        return 0
    
    df['hashtag_count'] = df['hashtag'].apply(count_hashes_in_row)
    
    # 計算總數
    total_hashtags = df['hashtag_count'].sum()
    
    # 打印結果
    print(f"`hashtag` 欄位內的 `#` 總數為：{total_hashtags}")
    
    # 將結果儲存到新文件
    output_file = "hashtag_count_output.csv"
    df.to_csv(output_file, index=False)
    print(f"包含 `hashtag_count` 的文件已儲存到：{output_file}")

# 執行程式
if __name__ == "__main__":
    count_hashtags(input_file)
