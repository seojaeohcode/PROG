import pandas as pd

def filter_and_save_esg_file():
    file_path = 'company_last.xlsx'  # 원본 파일 경로
    save_path = 'company_esg.xlsx'  # 필터링된 파일 경로

    # 데이터 로드
    df = pd.read_excel(file_path)

    # 시가총액 순서를 유지 (인덱스 기반 유지)
    filtered_df = df[~((df['지속가능경영보고서'] == 'X') | 
                       (df['기업지배구조보고서'] == 'X') | 
                       (df['채권발행이력수'] == 0))].copy()

    # 기존 인덱스 유지한 채 저장 (시총 순서 유지)
    filtered_df.to_excel(save_path, index=False)

    print(f"시가총액 순서를 유지한 채 필터링된 데이터가 {save_path}에 저장되었습니다.")

# 함수 실행 예제
filter_and_save_esg_file()
