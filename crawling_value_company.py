import FinanceDataReader as fdr
import pandas as pd

def get_top_market_cap_kospi(top_n=100):
    """
    KOSPI 시가총액 상위 top_n 개 기업을 조회하여 DataFrame으로 반환
    """
    # KOSPI 종목 데이터 불러오기
    kospi = fdr.StockListing('KOSPI')
    
    # 시가총액 내림차순 정렬 및 상위 top_n 추출
    kospi_sorted = kospi.sort_values(by="Marcap", ascending=False).head(top_n)
    
    # 필요한 컬럼만 정리
    result_df = kospi_sorted[['Code', 'Name', 'Marcap']].copy()
    
    # 시가총액을 원 단위로 변환 (기본 제공은 원 단위)
    result_df['Marcap'] = result_df['Marcap'].astype(int)
    
    return result_df

if __name__ == "__main__":
    # KOSPI 시가총액 상위 100개 종목 출력
    result_df = get_top_market_cap_kospi(100)
    print("KOSPI 시가총액 상위 100 종목:")
    print(result_df)

    # CSV로 저장 가능
    # result_df.to_csv("kospi_top100.csv", index=False)
