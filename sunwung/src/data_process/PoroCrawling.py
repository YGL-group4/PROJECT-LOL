"""
# -*- coding: utf-8 -*-
-----------------------------------------------------------------------------------
# Description:
1. 랭킹 페이지
2. 1~100위까지 소환사 이름 + 라인
3. 소환사 최근 20게임에서 게임 데이터 가져오기(승패, k/d/a, kda, cs/min, krate 추출)
4. 라인별로 dataframe 저장하기
5. xlsx 파일 저장(라인 별 sheet 분배)


# Author: Sunwung Lee
# DoC: 2021.05.23
-----------------------------------------------------------------------------------
# Reference: poro.gg
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

import pandas as pd
import re
import time

class PoroCrawling:
    # 소환사 이름 및 라인
    info_matches = {'탑': [], '정글': [], '미드': [], '원딜': [], '서포터': []}
    # 자료중 소환사명, 주포지션만 추출
    info_summoner = {'summoner': [], 'summoner_position': []}
    # 각 포지션별로 소환사명 정리
    positions = {'탑': [], '정글': [], '미드': [], '원딜': [], '서포터': []}

    def __init__(self):
        #
        # webdriver로 poro.gg 불러오기
        #
        path = chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(path)
        # 드라이버 오픈(3개의 드라이버를 열어 최대한 순위 변동의 변수를 없앰)
        self.driver.get("https://poro.gg/leaderboards")

    #
    # 1위부터 100위까지 최근 20경기 데이터 받아오기
    #
    def read_pages(self):
        # 각 랭커별 랭크, 소환사명, 티어, 랭크포인트, 승률, 승, 패, 레벨, 주포지션, 주챔피언
        info = '#wrapper > div > div > div.container.mt-4.p-0 > div.leaderboards-box.mt-4 > div.leaderboards-box__content > table > tbody > tr'
        self.top_1_to_100 = self.driver.find_elements_by_css_selector(info)
        self.driver.implicitly_wait(3)
        self.driver.get("https://poro.gg/leaderboards")
        print(f"홈페이지 로딩 끝")

    def read_matches(self):
        driver = self.driver
        for idx, info in enumerate(self.top_1_to_100):
            info_xpath = '//*[@id="wrapper"]/div/div/div[5]/div[1]/div[2]/table/tbody/tr[' + str(idx+1) +']'
            player_rank = driver.find_element_by_xpath(info_xpath + '/td[1]').text
            player_id = driver.find_element_by_xpath(info_xpath + '/td[2]/a/span').text
            player_role = driver.find_element_by_xpath(info_xpath + '/td[9]/img').get_attribute('alt')
            # 클릭하고 싶은 것 선택
            xpath = '//*[@id="wrapper"]/div/div/div[5]/div[1]/div[2]/table/tbody/tr[' + str(idx+1) + ']/td[2]/a'
            target = driver.find_element_by_xpath(xpath)
            target.send_keys(Keys.CONTROL +"\n")
            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(3)
            ## 솔로랭크 선택
            driver.find_element_by_xpath('//*[@id="vue-profile"]/div[3]/div[1]/div[2]/div/div[1]/button[2]').click()
            driver.implicitly_wait(3)
            #
            # poro.gg 소환사 최근 20게임에서 게임 데이터 가져오기
            #
            css_sel = '#vue-profile > div.match-history-container.mt-3 > div.mt-2'
            matches = driver.find_elements_by_css_selector(css_sel)
            # matches[0]: 최근 20게임 전적 요약
            # matches[1:]: 최근 20게임 게임 데이터
            matches = matches[1:]

            print(f"[{player_rank}등, {player_role}] {player_id} 님의 경기 결과 불러오기")
            for idx, match in enumerate(matches):
                item = BeautifulSoup(match.get_attribute('innerHTML'), 'html.parser')
                current_xpath = '//*[@id="vue-profile"]/div[3]/div[' + str(idx+1+2) + ']'
                role_xpath = current_xpath + '/div/div[2]/div[3]/div[2]/div[1]/div[' + str(self.convert_role_to_num(player_role)) + ' ]/a[2]/span'
                role = driver.find_element_by_xpath(role_xpath)

                ## 주 포지션으로 경기했는지 확인
                if role.text == player_id:
                    result = item.select('div.match-history__result > span')[0].text
                    time_xpath = current_xpath + '/div/div[2]/div[1]/div/span[3]'
                    kill_xpath = current_xpath + '/div/div[2]/div[2]/div[2]/div[1]/span[1]'
                    death_xpath = current_xpath + '/div/div[2]/div[2]/div[2]/div[1]/span[2]'
                    assist_xpath = current_xpath + '/div/div[2]/div[2]/div[2]/div[1]/span[3]'
                    kda_xpath = current_xpath + '/div/div[2]/div[2]/div[2]/div[2]/span'
                    krate_xpath = current_xpath + '/div/div[2]/div[2]/div[3]/div[1]/span[1]'
                    cs_xpath = current_xpath + '/div/div[2]/div[2]/div[3]/div[1]/span[2]'
                    cspm_xpath = current_xpath + '/div/div[2]/div[2]/div[3]/div[1]/span[3]'
                    vision_xpath = current_xpath + '/div/div[2]/div[2]/div[3]/div[1]/span[4]'

                    time = driver.find_element_by_xpath(time_xpath).text
                    kill = driver.find_element_by_xpath(kill_xpath).text
                    assist = driver.find_element_by_xpath(assist_xpath).text
                    death = driver.find_element_by_xpath(death_xpath).text
                    kda = driver.find_element_by_xpath(kda_xpath).text
                    krate = driver.find_element_by_xpath(krate_xpath).text
                    krate = krate.split('%')[0]
                    cs = driver.find_element_by_xpath(cs_xpath).text
                    cspm = driver.find_element_by_xpath(cspm_xpath).text
                    cspm = cspm.split('(')[1].split(')')[0].split('/')[0]
                    vision = driver.find_element_by_xpath(vision_xpath).text

                    # 경기 dictionary로 저장
                    one_match_info = dict(zip(['rank', 'id', 'time', 'kill', 'death', 'assist', 'kda', 'krate', 'cs', 'cspm', 'vision', 'result'],
                                              [int(player_rank), player_id, time, int(kill), int(death), int(assist), kda, float(krate), int(cs), float(cspm), int(vision), result]))
                    #print(f"{idx+1}경기, 결과: {result}, 경기시간: {time}, {kill}/{death}/{assist}, KDA: {kda}, 킬관여: {krate}, cs: {cs}, 분당cs: {cspm}, 시야점수: {vision}") # WILL DELETE
                    # role 배열에 저장
                    self.info_matches[player_role].append(one_match_info)
                else:
                    pass
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    def convert_role_to_num(self, role):
        role_num = 0
        if role == "탑":
            role_num = 1
        elif role == "정글":
            role_num = 2
        elif role == "미드":
            role_num = 3
        elif role == "원딜":
            role_num = 4
        elif role == "서포터":
            role_num = 5
        else:
            pass
        return role_num

    def close_driver(self):
        self.driver.close()
        print(f"프로그램을 마칩니다.")

    def save_xlsx(self):
        #
        # dataframe 형식으로 저장.
        #
        df_top = pd.DataFrame(self.info_matches['탑'])
        df_jug = pd.DataFrame(self.info_matches['정글'])
        df_mid = pd.DataFrame(self.info_matches['미드'])
        df_adc = pd.DataFrame(self.info_matches['원딜'])
        df_sup = pd.DataFrame(self.info_matches['서포터'])

        #
        # 엑셀 파일로 저장(sheet 별)
        #
        import datetime as dt
        x = dt.datetime.now()
        x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond
        date = str(x.year) + '-' + str(x.month) + '-' + str(x.day)

        filepath = "C:\\Users\\User\\Desktop\\python\\0_group_project\\group4_first\\"
        filename = f"{date}_top_1_to_100_by_role"
        print(f"{filename}.xlsx 파일을 생성합니다.")
        writer = pd.ExcelWriter(f"{filepath + filename}.xlsx", engine='xlsxwriter')

        df_top.to_excel(writer, index=None, sheet_name='탑')
        df_jug.to_excel(writer, index=None, sheet_name='정글')
        df_mid.to_excel(writer, index=None, sheet_name='미드')
        df_adc.to_excel(writer, index=None, sheet_name='원딜')
        df_sup.to_excel(writer, index=None, sheet_name='서포터')

        writer.save()
        print(f"파일 생성 완료")



if __name__ == '__main__':
    try:
        test = PoroCrawling()
        test.read_pages()
        test.read_matches()
        test.close_driver()
        print(f"아이디 및 라인 받아오기 끝")

        print("크롤링 완료")
    except KeyboardInterrupt:
        print("hi")
