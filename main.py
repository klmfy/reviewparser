from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from fake_useragent import UserAgent
import pandas as pd
import time
import random

link = "https://top20.ua/ru/kh/restorani-kafe-bari/restorani/puri-chveni.html#company_reviews_list"
# link = "https://top20.ua/ru/kh/restorani-kafe-bari/restorani/pervaya-chayhana.html"
data = []
nickname = []
stat = []
scores = []
emotions = []
comments = []
photo = []
replys = []
kitchen = []
obslug = []
atmosphere = []
place = []
cost = []

useragent = UserAgent()

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", useragent.random)
driver = webdriver.Firefox(options=options)
driver.get(link)

try:
    wait = WebDriverWait(driver, 30)

    # button = driver.find_element(By.XPATH, ".//*[@class='btn btn-lg see_all js-more']")
    # button.click()
    # time.sleep(0.7)  # Adjust the sleep duration as needed for elements to load

    try:
        while True:
            try:
                button = driver.find_element(By.XPATH, ".//*[@class='btn btn-lg see_all js-more']")
                button.click()
                time.sleep(0.7)  # Adjust the sleep duration as needed for elements to load
                try:
                    button_comment = driver.find_element(By.XPATH,
                                                         ".//*[@class='media-body']/div[@class='media-text']/a")
                    button_comment.click()
                except:
                    pass
            except:
                break
    except:
        pass

    # Wait for all elements to be present
    blocks = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                ".//div[@class='media']",
            )
        )
    )

    # Process each block and extract data
    for block in blocks:
        time.sleep(0.2)
        try:
            try:
                date_element = block.find_element(By.XPATH, ".//div[@class='media-body']/div[@class='media-heading d-sm-flex align-items-center']/div[@class='comment-data ml-sm-auto']")
                date = date_element.text.strip()
                list_month = {"января": '01', "февраля": '02', "марта": '03', "апреля": '04', "мая": '05', "июня": '06',
                              "июля": '07', "августа": '08', "сентября": '09', "октября": '10', "ноября": '11',
                              "декабря": '12'}
                for month, num in list_month.items():   #обработка с "20 сентября 2021" в "20.09.2021"
                    if month in date:
                        date = date.replace(month, num).replace(" ", ".")
                data.append(date)
                print(date)

                try:
                    name_element = block.find_element(By.XPATH, ".//div[@class='media-left']/span")
                    name = name_element.text.strip()
                    nickname.append(name)

                    stat.append("-")
                    photo.append("-")

                    print(name)

                    try:
                        score_element = block.find_element(By.XPATH, ".//div[@class='media-body']/div[@class='media-heading d-sm-flex align-items-center']/div[@class='company_page-group']/div[@class='company_page--top']/div/span[2]")
                        score = score_element.text.strip()
                        score = float(score)
                        print(type(score))
                        scores.append(round(score))
                        print(score)
                        def random_choice(arg):
                            random_choice = random.choice([arg, "-"])
                            return random_choice
                        if int(score) == 1:
                            emotions.append("Негативні")
                            kitchen.append("Не сподобалось")
                            obslug.append("Я обурений")
                            atmosphere.append(random_choice("Не сподобалось"))
                            place.append(random_choice("Не зручно"))
                            cost.append("Завишені")
                        if int(score) == 2:
                            emotions.append("Більш негативні")
                            kitchen.append("Не сподобалось")
                            obslug.append("Не сподобалось")
                            atmosphere.append(random_choice("Не сподобалось"))
                            place.append(random_choice("Не зручно"))
                            cost.append("Завишені")
                        if int(score) == 3:
                            emotions.append("Нормально")
                            kitchen.append("Посередньо")
                            obslug.append("Посередньо")
                            atmosphere.append(random_choice("Cподобалось"))
                            place.append(random_choice("-"))
                            cost.append("Нормальні")
                        if int(score) == 4:
                            emotions.append("Більш позитивні")
                            kitchen.append("Смачно")
                            obslug.append("Сподобалось")
                            atmosphere.append(random_choice("Cподобалось"))
                            place.append(random_choice("Зручно"))
                            cost.append("Адекватні")
                        if int(score) == 5:
                            emotions.append("Позитивні")
                            kitchen.append("Дуже смачно")
                            obslug.append("Дуже сподобалось")
                            atmosphere.append(random_choice("Cподобалось"))
                            place.append("Зручно")
                            cost.append("Приємні")

                        try:
                            try:
                                comment_element = block.find_element(By.XPATH,
                                                                  ".//div[@class='media-body']/div[@class='media-text open']/span[@class='full_review']")
                                comment = comment_element.text.strip()
                                comments.append(comment)
                                print(comment)
                            except:
                                comment_element = block.find_element(By.XPATH,
                                                                     ".//div[@class='media-body']/div[@class='media-text']")
                                comment = comment_element.text.strip()
                                comments.append(comment)
                                print(comment)
                            try:
                                reply_element = block.find_element(By.XPATH,
                                                                     ".//div[@class='media-body']/div[@class='media media-next']/div[@class='media-descrition']")
                                reply = reply_element.text.strip()
                                replys.append(reply)
                                print(reply)
                            except Exception as e:
                                print("-")
                                replys.append("-")

                        except Exception as e:
                            print(f"Unable to extract comment for the block. Error: {e}")

                    except Exception as e:
                        print(f"Unable to extract score for the block. Error: {e}")

                except Exception as e:
                    print(f"Unable to extract name for the block. Error: {e}")

            except Exception as e:
                print(f"Unable to extract date for the block. Error: {e}")

        except:
            print("Ошибка", block)
except Exception as e:
    print("Произошла ошибка:", e)

finally:
    print(len(data), len(nickname), len(scores), len(comments), len(replys), len(stat), len(emotions), len(photo), len(kitchen), len(obslug), len(atmosphere), len(place), len(cost))
    # emotions.append("Негативні")
    #     kitchen.append("Не сподобалось")
    #     obslug.append("Я обурений")
    #     atmosphere.append(random_choice("Не сподобалось"))
    #     place.append(random_choice("Не зручно"))
    #     cost.append("Завишені")
    df = pd.DataFrame({'Дата': data,
                      'Нікнейм': nickname,
                      'Стать': stat,
                      'Оцінка': scores,
                      'Емоції': emotions,
                      'Коментар': comments,
                      'Фото': photo,
                      'Зворотня реакція': replys,
                      'Кухня': kitchen,
                      'Обслуговування':obslug,
                      'Атмосфера': atmosphere,
                      'Розташування': place,
                      'Ціна': cost})
    df.to_excel('example.xlsx')
    driver.quit()
