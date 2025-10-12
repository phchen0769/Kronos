import tushare as ts
import pandas as pd
from datetime import datetime
import os

class HKStockDownloader:
    def __init__(self, token):
        """
        初始化港股数据下载器
        """
        self.token = token
        self.pro = None
        self._initialize()
    
    def _initialize(self):
        """
        初始化 Tushare
        """
        try:
            ts.set_token(self.token)
            self.pro = ts.pro_api()
            print("✅ Tushare 初始化成功")
        except Exception as e:
            print(f"❌ Tushare 初始化失败：{str(e)}")
            return False
        return True
    
    def download_hk_data(self, symbol, start_date, end_date):
        """
        下载港股数据
        """
        # 检查初始化状态
        if self.pro is None:
            print("❌ Tushare 未正确初始化")
            return None, None
        
        try:
            print("⏳ 正在下载港股数据...")
            
            # 下载数据
            df = self.pro.hk_daily(
                ts_code=f'{symbol}.HK',
                start_date=start_date,
                end_date=end_date
            )
            
            if len(df) == 0:
                print("⚠️  未获取到数据，请检查参数")
                return None, None
            
            # 按日期排序
            df = df.sort_values('trade_date')
            
            # 创建数据目录
            data_dir = "stock_data"
            os.makedirs(data_dir, exist_ok=True)
            
            # 保存数据
            filename = f"{data_dir}/HK_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"✅ 数据下载完成！")
            print(f"📊 共下载 {len(df)} 条记录")
            
            return df, filename
            
        except Exception as e:
            print(f"❌ 下载失败：{str(e)}")
            return None, None

# 使用示例
if __name__ == "__main__":
    # 创建下载器实例
    downloader = HKStockDownloader('b60097683092d0167722ddbe7b9b5ed184d5dd2dbec7df446d4feec7')
    
    # 下载数据 - 使用安全的方式
    result = downloader.download_hk_data(
        symbol='00939',
        start_date='20240101',
        end_date='20241010'  # 修改为当前可用的日期
    )
    
    # 检查返回值
    if result is None:
        print("下载失败，返回 None")
    elif isinstance(result, tuple) and len(result) == 2:
        data, file_path = result
        if data is not None:
            print(f"\n📋 数据详情：")
            print(f"   数据期间：{data['trade_date'].min()} 至 {data['trade_date'].max()}")
            
            # 显示数据基本信息
            print(f"\n🔍 数据统计：")
            print(f"   数据条数：{len(data)}")
            print(f"   保存路径：{file_path}")
            
            # 显示前几条数据
            print(f"\n📄 数据预览：")
            print(data.head(10))
        else:
            print("数据为空")
    else:
        print("下载失败，返回意外的结果")