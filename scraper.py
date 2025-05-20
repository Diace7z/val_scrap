import mainbar
import sidebar
import page_avaible
import sys_sampling
import link_id
import pandas as pd
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from IPython.display import clear_output
import re
import matplotlib.pyplot as plt
from cleaning_module import val_clean
#//*[@id="oqbP7"] [verify]

def human_delay(min_time=1.5, max_time=4):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)

data_columns = ['link','rating','level','win_lose','playtime','dmg_round','kd_ratio','hs_rate',
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
                  'map_name_5','map_wr_5','map_win_lose_5','map_name_6','map_wr_6','map_win_lose_6','map_name_7','map_wr_7','map_win_lose_7']

def div_n(driver):
    n_m = 3
    path =  f'//*[@id="app"]/div[2]/div[3]/div/main/div[{n_m}]'
    try: 
        respon = driver.find_element(By.XPATH, value = path).text
        if ('private' in respon.lower()) or ('not found' in respon.lower()) or ('error' in respon.lower()) or ('overview' in respon.lower()):
            n_m = 3
        else :
            n_m = 4
    except Exception as e:
        n_m = 4
    return n_m

def scraper (filename, r = 1, ep_act = 'V25A2', error = 'n', prefix = '', sampling = 'sys', main = 'yes'):
    df = pd.read_csv(filename)
    try:
        overview = pd.read_csv("overview_"+prefix+filename, low_memory=False)
        overview = np.array(overview)
        overview = list(overview)
        start = len(overview)
        print('file found')
    except:
        overview = []
        start = 0
        print('file not found')

    # Random sampling type
    if sampling == 'systematic':
        ids = sys_sampling.sys_sampling(list(df['id']), r)
        n_link = [ link_id.link_id(x,ep_act) for x in ids]
    else :
        ids = random.sample(list(df['id']), r*len(df))
        n_link = [ link_id.link_id(x,ep_act) for x in ids]
    
    print('size of data:', len(n_link))
    count = 0 + start
    acm_time = 0
    driver = uc.Chrome(headless=False,use_subprocess=True)
    driver.maximize_window()
    for link in n_link[start:]:
        try:
            t0 = time.time()
            persen = int((count*100)/(len(n_link)))
            loading_bar = ["█" for x in range(persen)] + ["|" for x in range(100 - persen) ]
            print(''.join(loading_bar),persen,'%')
            print('Player no.',count, )
            try:
                
                driver = page_avaible.page_available(link,driver, main)
            except: 
                driver.quit()
                driver = page_avaible.page_available(link,driver, main)
            n = div_n(driver)
            record = [link] + mainbar.mainbar(driver,dv_num = n, error = error) + sidebar.sidebar(driver,dv_num = n, error = error)
            overview.append(record)
            df = pd.DataFrame(overview)
            df.columns = data_columns
            if count % 10 == 0:
                clear_output(wait=True)
                rating = df['rating'].apply(lambda x: 'Radiant' if 'Radiant' in str(x) else re.findall(r'Immortal \d+', str(x))[0] if                                                   'Immortal' in str(x) else str(x).replace('Rating\n','') if
                                         'Rating\n' in str(x) else x)
                rating.value_counts(normalize=False).plot(kind='bar', figsize=(8, 4), color='skyblue')
                plt.show()
            df.to_csv("overview_"+prefix+filename,  index = False)
            human_delay(5,10)
            count+=1
            print("Scrap duration:",time.time()-t0)
            acm_time += time.time()-t0
            print(acm_time)
            #driver.quit()
        except Exception as e:
            print(e)
            driver.quit()
            driver = uc.Chrome(headless=False,use_subprocess=True)
            driver.maximize_window()
    clear_output(wait=True)
    loading_bar = ["█" for x in range(100)] 
    print(''.join(loading_bar),persen,'%')
    driver.quit()
    df = pd.DataFrame(overview)
    df.columns = data_columns
    df.to_csv("overview_"+prefix+filename,  index = False)

    
        


