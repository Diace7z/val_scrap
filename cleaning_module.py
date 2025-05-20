def val_clean(df):
    """
    ['link','rating','level','win_lose','playtime','dmg_round','kd_ratio','hs_rate',
                  'win_rate','wins','kast','deal_receive','kills','deaths','assists'
                  ,'acs','kad_ratio','kill_per_round','first_blood','flawless','aces',
                  'round_win%','kast_score','acs_score','agent1','matches1','win_rate1',
                  'k_d_ratio1','adr_1','acs1','d_receive1','map_agent_1','agent2','matches2',
                  'win_rate2','k_d_ratio2','adr_2','acs2','d_receive2','map_agent_2','agent3',
                  'matches3','win_rate3','k_d_ratio3','adr_3','acs3','d_receive3','map_agent_3',
                  'tracker_score','past_tier','past_episode','head_rate','head_hits','body_rate',
                  'body_hits','legs_rate','legs_hits','role_1','wrate_initiator','win_lose_initiator','kda_rate_initiator',
                  'kda_num_initiator','role_2','wrate_duelist','win_lose_duelist','kda_rate_duelist','kda_num_duelist',
                  'role_3','wrate_controller','win_lose_controller','kda_rate_controller','kda_num_controller',
                  'role_4','wrate_sentinel','win_lose_sentinel','kda_rate_sentinel','kda_num_sentinel',
                  'wp_name_1','wp_type_1','wp_head_rate_1','wp_body_rate_1','wp_legs_rate_1','wp_kills_1',
                  'wp_name_2','wp_type_2','wp_head_rate_2','wp_body_rate_2','wp_legs_rate_2','wp_kills_2',
                  'wp_name_3','wp_type_3','wp_head_rate_3','wp_body_rate_3','wp_legs_rate_3','wp_kills_3',
                  'map_name_1','map_wr_1','map_win_lose_1','map_name_2','map_wr_2','map_win_lose_2',
                  'map_name_3','map_wr_3','map_win_lose_3','map_name_4','map_wr_4','map_win_lose_4',
                  'map_name_5','map_wr_5','map_win_lose_5','map_name_6','map_wr_6','map_win_lose_6',
                  'map_name_7','map_wr_7','map_win_lose_7']
    """
    import pandas as pd
    import re


    #Ambil kolom numerik
    selected_columns = ['level','playtime','dmg_round','kd_ratio','hs_rate','win_rate','wins','kast',
                        'deal_receive','kills','deaths','assists','acs','kad_ratio','kill_per_round','first_blood',
                        'flawless','aces','round_win%','kast_score','acs_score']
    for col in selected_columns:
        # Ensure all values are converted to strings before applying regex
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x)[0:str(x).find('Top')] if 'Top' in str(x) else str(x)[0:str(x).find('Bottom')] if 'Bottom' in str(x) else str(x))
            df[col] = df[col].apply(lambda x: str(x).replace(',',''))
            df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
        else:
            print("No column found")


    ####################################################################################################

    #Agent section cleaning
    selected_columns =['agent1','matches1','win_rate1','k_d_ratio1','adr_1','acs1','d_receive1','map_agent_1',
                       'agent2','matches2','win_rate2','k_d_ratio2','adr_2','acs2','d_receive2','map_agent_2',
                       'agent3','matches3','win_rate3','k_d_ratio3','adr_3','acs3','d_receive3','map_agent_3']
    for col in selected_columns:
        if 'agent' not in col:
            df[col] = df[col].apply(lambda x: str(x)[0:str(x).find('Top')] if 'Top' in str(x) else str(x)[0:str(x).find('Bottom')] if 'Bottom' in str(x) else str(x))
            df[col] = df[col].apply(lambda x: str(x).replace(',',''))
            df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
        else:
            df[col] = df[col].apply(lambda x: str(x).split('\n') if '\n' in str(x) else str(x))
            if 'hours' in str(col):
                df[col+'_name'] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_hours'] = df[col].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_hours'] = df[col+'_hours'].apply(lambda x: str(x).replace(',',''))
                df[col+'_hours'] = df[col+'_hours'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_hours'] = df[col+'_hours'].apply(pd.to_numeric, errors='coerce')
            else:
                df[col+'_name'] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_wr'] = df[col].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_wr'] = df[col+'_wr'].apply(lambda x: str(x).replace(',',''))
                df[col+'_wr'] = df[col+'_wr'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_wr'] = df[col+'_wr'].apply(pd.to_numeric, errors='coerce')
    
    #Accuracy section cleaning
    selected_columns = ['head_rate','head_hits','body_rate','body_hits','legs_rate','legs_hits']
    for col in selected_columns:
        df[col] = df[col].apply(lambda x: str(x)[0:str(x).find('Top')] if 'Top' in str(x) else str(x)[0:str(x).find('Bottom')] if 'Bottom' in str(x) else str(x))
        df[col] = df[col].apply(lambda x: str(x).replace(',',''))
        df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
        df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    #Role section cleaning
    
    selected_columns = ['wrate_initiator','win_lose_initiator','kda_rate_initiator','kda_num_initiator',
                       'wrate_duelist','win_lose_duelist','kda_rate_duelist','kda_num_duelist',
                          'wrate_controller','win_lose_controller','kda_rate_controller','kda_num_controller',
                            'wrate_sentinel','win_lose_sentinel','kda_rate_sentinel','kda_num_sentinel']
    for col in selected_columns:
        if 'win_lose_' in col or 'kda_num_' in col:
            if 'Kda_num_' in col:
                df[col] = df[col].apply(lambda x: str(x).split('/') if '/' in str(x) else str(x))
                df[col+'_kills'] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_kills'] = df[col+'_kills'].apply(lambda x: str(x).replace(',',''))
                df[col+'_kills'] = df[col+'_kills'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_kills'] = df[col+'_kills'].apply(pd.to_numeric, errors='coerce')
                df[col+'_deaths'] = df[col].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_deaths'] = df[col+'_deaths'].apply(lambda x: str(x).replace(',',''))
                df[col+'_deaths'] = df[col+'_deaths'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_deaths'] = df[col+'_deaths'].apply(pd.to_numeric, errors='coerce')
                df[col+'_assists'] = df[col].apply(lambda x: x[2] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_assists'] = df[col+'_assists'].apply(lambda x: str(x).replace(',',''))
                df[col+'_assists'] = df[col+'_assists'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_assists'] = df[col+'_assists'].apply(pd.to_numeric, errors='coerce')
            else:
                df[col] = df[col].apply(lambda x: str(x).split('-') if '-' in str(x) else str(x))
                df[col+'_win'] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_win'] = df[col+'_win'].apply(lambda x: str(x).replace(',',''))
                df[col+'_win'] = df[col+'_win'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_win'] = df[col+'_win'].apply(pd.to_numeric, errors='coerce')

                df[col+'_lose'] = df[col].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else x)
                df[col+'_lose'] = df[col+'_lose'].apply(lambda x: str(x).replace(',',''))
                df[col+'_lose'] = df[col+'_lose'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
                df[col+'_lose'] = df[col+'_lose'].apply(pd.to_numeric, errors='coerce')
        else:
            df[col] = df[col].apply(lambda x: str(x).replace(',',''))
            df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
            df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    #Weapon section cleaning
    selected_columns = ['wp_head_rate_1','wp_body_rate_1','wp_legs_rate_1','wp_kills_1',
                          'wp_head_rate_2','wp_body_rate_2','wp_legs_rate_2','wp_kills_2',
                          'wp_head_rate_3','wp_body_rate_3','wp_legs_rate_3','wp_kills_3']
    for col in selected_columns:
        df[col] = df[col].apply(lambda x: str(x).replace(',',''))
        df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
        df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    #Map section cleaning
    selected_columns = ['map_wr_1', 'map_wr_2', 'map_wr_3', 'map_wr_4', 'map_wr_5', 'map_wr_6', 'map_wr_7']
    for col in selected_columns:
        df[col] = df[col].apply(lambda x: str(x).replace(',',''))
        df[col] = df[col].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
        df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    
    selected_columns = ['map_win_lose_1','map_win_lose_2','map_win_lose_3','map_win_lose_4',
                       'map_win_lose_5','map_win_lose_6','map_win_lose_7']
    for col in selected_columns:
        df[col] = df[col].apply(lambda x: str(x).split('-') if '-' in str(x) else str(x))
        df[col+'_win'] = df[col].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
        df[col+'_win'] = df[col+'_win'].apply(lambda x: str(x).replace(',',''))
        df[col+'_win'] = df[col+'_win'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
        df[col+'_win'] = df[col+'_win'].apply(pd.to_numeric, errors='coerce')

        df[col+'_lose'] = df[col].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 0 else x)
        df[col+'_lose'] = df[col+'_lose'].apply(lambda x: str(x).replace(',',''))
        df[col+'_lose'] = df[col+'_lose'].apply(lambda x: float(re.findall(r'\d+\.\d+', str(x))[0]) if re.findall(r'\d+\.\d+', str(x)) else  float(re.findall(r'\d+', str(x))[0]) if re.findall(r'\d+', str(x)) else x)
        df[col+'_lose'] = df[col+'_lose'].apply(pd.to_numeric, errors='coerce')


    # Merapihkan kolom rating 
    df['rating'] = df['rating'].apply(lambda x: 'Radiant' if 'Radiant' in str(x) else re.findall(r'Immortal \d+', str(x))[0] if 'Immortal' in str(x) else str(x).replace('Rating\n','') if
                                        'Rating\n' in str(x) else x)
        

    #Membuat kolom matches
    df['matches'] =     df['win_lose'].apply(lambda x: float(re.findall(r'\d+',str(x))[0])+float(re.findall(r'\d+',str(x))[1]) if re.findall(r'\d+',str(x)) else float('nan'))
    df['mathces_win'] = df['win_lose'].apply(lambda x: float(re.findall(r'\d+',str(x))[0]) if re.findall(r'\d+',str(x)) else float('nan'))
    df['mathces_lose'] = df['win_lose'].apply(lambda x: float(re.findall(r'\d+',str(x))[1]) if re.findall(r'\d+',str(x)) else float('nan'))
    df['matches'] = df['matches'].apply(pd.to_numeric, errors='coerce') #Memastikan kolom matches menjadi numerik atau NaN jika tidak bisa dikonvers
    df['mathces_win'] = df['mathces_win'].apply(pd.to_numeric, errors='coerce') #Memastikan kolom matches menjadi numerik atau NaN jika tidak bisa dikonvers    
    df['mathces_lose'] = df['mathces_lose'].apply(pd.to_numeric, errors='coerce') #Memastikan kolom matches menjadi numerik atau NaN jika tidak bisa dikonvers
    # Drop kolom win_lose karena sudah tidak diperlukan
    df = df.drop(columns=['win_lose'])

    #Membuat flex_rate_wp1, flex_rate_wp2, flex_rate_wp3, flex_rate_wp: menilai seberapa sering senjata digunakan dibandingkan dengan total kill
    df['flex_rate_wp1'] = df.loc[:,'wp_kills_1'] / df.loc[:,'kills'] * 100
    df['flex_rate_wp2'] = df.loc[:,'wp_kills_2'] / df.loc[:,'kills'] * 100
    df['flex_rate_wp3'] = df.loc[:,'wp_kills_3'] / df.loc[:,'kills'] * 100
    df['flex_rate_wp']  = df[['wp_kills_1','wp_kills_2','wp_kills_3']].sum(axis=1)/df.loc[:,'kills'] * 100

    #Drop kolom non-ratio
    drop_columns = ['role_1','role_2','role_3','role_4']
    df = df.drop(columns=drop_columns)
    df.to_csv('df_cleaned.csv', index = False )
    display(df.head(10))
    return df
