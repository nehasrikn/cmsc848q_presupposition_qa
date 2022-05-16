import pandas as pd

def raw_to_cleaned():
    df = pd.read_csv('q_with_preds.csv')
    df = df.drop(columns=['document'])

    indices = []
    for _, row in df.iterrows():
        q = row['question']
        p = row['predicate']

        try:
            index = q.split(' ').index(p)
        except ValueError:
            index = -1

        indices.append(index)


    df['predicate_index'] = indices  
    output = df.to_csv(index=False)

    with open('cleaned_questions_0.csv', 'w') as f:
        f.write(output)


def separate_cleaned(clean_file='cleaned_questions.csv'):
    df = pd.read_csv(clean_file)
