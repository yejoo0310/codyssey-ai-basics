import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
TEST_CSV = os.path.join(BASE_DIR, 'spaceship-titanic/test.csv')
TRAIN_CSV = os.path.join(BASE_DIR, 'spaceship-titanic/train.csv')


def read_csv(path):
    try:
        file = pd.read_csv(path)
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
    df_test = read_csv(TEST_CSV)
    if df_test is None:
        return
    df_train = read_csv(TRAIN_CSV)
    if df_train is None:
        return
    data = pd.concat([df_test, df_train], ignore_index=True)
    print(data.shape)

    df_train['Transported'] = df_train['Transported'].astype(int)
    df_train = df_train.drop(['PassengerId', 'Name', 'Cabin'], axis=1)
    categorical_cols = df_train.select_dtypes(
        include=['object', 'bool']).columns.tolist()
    df_encoded = pd.get_dummies(
        df_train, columns=categorical_cols, dtype=int, dummy_na=True)
    correlations = df_encoded.corr()['Transported'].drop(
        'Transported').sort_values(ascending=False)
    print('Transported 항목과의 관련성')
    print(correlations)

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    labels = ['10대 미만', '10대', '20대', '30대', '40대', '50대', '60대', '70대']
    df_train['AgeGroup'] = pd.cut(
        df_train['Age'], bins=bins, labels=labels, right=False)
    transported_rate_by_age = df_train.groupby(
        'AgeGroup', observed=False)['Transported'].mean().reset_index()

    plt.rcParams['font.family'] = 'AppleGothic'
    plt.figure(figsize=(10, 6))
    plt.bar(transported_rate_by_age['AgeGroup'],
            transported_rate_by_age['Transported'])

    plt.title('나이대별 Transported 여부 비율')
    plt.xlabel('Age Group')
    plt.ylabel('Transported Rate')

    plt.show()


if __name__ == '__main__':
    main()
