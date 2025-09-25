import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
CSV_FILE = os.path.join(
    BASE_DIR, '성__연령_및_가구주와의_관계별_인구__시군구_20250923160231.csv')


def read_csv(path):
    try:
        file = pd.read_csv(path, encoding='utf-8')
        return file
    except FileNotFoundError:
        print(f'{path} 파일이 없습니다.')
        return None
    except UnicodeDecodeError:
        print('디코딩 오류가 발생했습니다.')
        return None
    except Exception as e:
        print(f'데이터를 읽는 중 알 수 없는 오류가 발생했습니다: {e}')
        return None


def main():
    df = read_csv(CSV_FILE)
    if df is None:
        return

    keep_columns = ['성별', '연령별', '시점', '일반가구원']
    drop_columns = [col for col in df.columns if col not in keep_columns]
    df = df.drop(drop_columns, axis=1)

    print('<남자 및 여자의 연도별 일반가구원 데이터 통계>')
    df_gender = df.loc[(df['성별'].isin(['남자', '여자'])) & (df['연령별'] == '합계')].drop(
        '연령별', axis=1).reset_index(drop=True)
    print(df_gender.to_string(index=False))

    print('\n' + '<연령별 일반가구원 데이터 통계>')
    df_age = df.loc[~df['연령별'].isin(['15~64세', '65세이상', '합계'])]
    df_age = df_age.groupby('연령별', as_index=False, sort=False)['일반가구원'].sum()
    print(df_age.to_string(index=False))

    df_gender_age = df.loc[(~df['연령별'].isin(['15~64세', '65세이상', '합계'])) & (
        df['성별'].isin(['남자', '여자']))]
    df_gender_age = df_gender_age.groupby(
        ['성별', '연령별'], as_index=False, sort=False)['일반가구원'].sum()

    plt.rcParams['font.family'] = 'AppleGothic'
    plt.figure(figsize=(15, 5))

    df_male = df_gender_age[df_gender_age['성별'] == '남자']
    plt.plot(df_male['연령별'], df_male['일반가구원'],
             color='blue', linestyle='-', marker='o', label='남자')

    df_female = df_gender_age[df_gender_age['성별'] == '여자']
    plt.plot(df_female['연령별'], df_female['일반가구원'],
             color='red', linestyle='-', marker='o', label='여자')

    plt.title('남자 및 여자의 연령별 일반가구원 데이터 통계')
    plt.xlabel('연령별')
    plt.ylabel('일반가구원')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
