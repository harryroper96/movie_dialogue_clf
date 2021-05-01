#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def load_csv_files():
    
    lines_col_names = ['line_id', 'character_id', 'movie_id', 'character_name', 'line']
    lines_df = pd.read_csv('cornell_movie_dialogs_corpus/movie_lines.txt', sep=' \+\+\+\$\+\+\+ ', 
                           engine='python', header=None, names=lines_col_names)
    
    movies_col_names = ['movie_id', 'movie', 'release_date', 'rating', 'votes', 'genres']
    movies_df = pd.read_csv('cornell_movie_dialogs_corpus/movie_titles_metadata.txt',
                            sep=' \+\+\+\$\+\+\+ ', engine='python', header=None, names=movies_col_names)
    
    conversations_col_names = ['character_one_id', 'character_two_id', 'movie_id', 'conversation']
    conversations_df = pd.read_csv('cornell_movie_dialogs_corpus/movie_conversations.txt',
                            sep=' \+\+\+\$\+\+\+ ', engine='python', header=None, names=conversations_col_names)
    conversations_df['conversation_id'] = ['c' + str(i) for i in range(len(conversations_df))]
    conversations_df['conversation'] = conversations_df['conversation'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    
    return lines_df, movies_df, conversations_df


def process_conversations(conversations_df, lines_df):
    
    split_df = conversations_df['conversation'].str.split(' ', n=None, expand=True)
    split_df = pd.concat([conversations_df['conversation_id'], split_df], axis=1)
    split_df = pd.melt(split_df, id_vars='conversation_id', var_name='line_pos', value_name='line_id')
    split_df = split_df.sort_values(by=['conversation_id', 'line_pos'], ascending=True)
    split_df.dropna(inplace=True)
    split_df = split_df.reset_index(drop=True)
    
    join_df = split_df.merge(lines_df[['line_id', 'line']], on='line_id', how='left')
    join_df.dropna(subset=['line'], inplace=True)
    join_df['dialogue'] = join_df.groupby('conversation_id')['line'].transform(lambda x: ' '.join(x))
    join_df = join_df[['conversation_id', 'dialogue']].drop_duplicates().reset_index(drop=True)
    
    lookup_df = conversations_df[['movie_id', 'conversation_id']].merge(join_df, on='conversation_id', how='left')

    return lookup_df


def create_final_df(movies_df, lookup_df):
    
    final_df = movies_df[['movie_id', 'movie', 'genres']].merge(lookup_df[['movie_id', 'dialogue']],
                                                                on='movie_id', how='left')
    final_df['genres'] = final_df['genres'].replace('[^a-zA-Z,]', '', regex=True)
    final_df = final_df.replace('', np.nan)
    final_df.dropna(subset=['genres', 'dialogue'], inplace=True)
    
    return final_df


def save_data(final_df):
    
    engine = create_engine('sqlite:///dialogue.db')
    final_df.to_sql('dialogue', engine, index=False, if_exists='replace')
    


def main():
    
    print('Loading data...')
    lines_df, movies_df, conversations_df = load_csv_files()
    print('Data loaded successfully.')
    time.sleep(1)
    
    print('Processing conversations...')
    lookup_df = process_conversations(conversations_df, lines_df)
    print('Conversations processed successfully.')
    time.sleep(1)
    
    print('Creating dataframe...')
    final_df = create_final_df(movies_df, lookup_df)
    print('Dataframe created successfully.')
    time.sleep(1)
    
    print('Saving data...')
    save_data(final_df)
    print('Data saved successfully to ./dialogue.db')
    


if __name__ == '__main__':
    main()

