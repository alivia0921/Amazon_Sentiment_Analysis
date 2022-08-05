#https://www.amazon.in/Spirili-Rechargable-Console-Screen-Classic/product-reviews/B07VC4N1LM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
#https://www.amazon.in/SpinBot-BattleMods-Conductive-Triggers-etc-Supports/product-reviews/B0823H4Y4X/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
#https://www.amazon.in/s?k=gaming+device&ref=nb_sb_noss_2 
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from textblob import TextBlob

textL = []
scoreL = []
review_content = []
# link = input("Enter an amazon link: ")

def scrape(link, sure):
  global page
  global soup
  global rev
  if sure == "yes": 
    page = requests.get(link)
    soup = bs(page.content, 'html.parser')

    review = soup.find_all("span",{"data-hook":"review-body"})
    for i in range(0,len(review)):
      review_content.append(review[i].get_text())
    # print(review_content)

    review_content[:] = [reviews.lstrip('\n') for reviews in review_content]
    review_content[:] = [reviews.rstrip('\n') for reviews in review_content]

  else: 
    Exit = input("Do you want to exit the program? ")
    if Exit == "yes":
      print("Thanks for using!")
      exit()
    else: 
      link = input("please enter the Amazon product's link that you want to analyze: ")
      sure = input("Are you sure to analyze this link: ")
      scrape(link, sure)
    # print(review_content)

def store():
  global count, score, average, eachScore
  count = 0
  score = 0
  for text in review_content:
    post = TextBlob(text)
    # print(text)
    textL.append(text)
    eachScore = post.sentiment.polarity
    # print(post.sentiment.polarity)
    scoreL.append(eachScore)
    score += post.sentiment.polarity
    count += 1

  average = score/count



def openF():
  with open("scores", "w") as fout:
    for i in range(len(textL)):
      fout.write(str(textL[i]))
      fout.write(": ")
      fout.write(str(scoreL[i]))
      fout.write("\n\n")


def result(average):

  print("\n" + "The score will be ranked from -1 to 1, from the lowest to the highest." + "\n")

  if average <= 0.99: 
    print("The average review score for this product is: " + str(average) + ". This product might not be the best option, please reconsider about it.")
  elif average <= 0.3: 
    print("The average review score for this product is: " + str(average) + ". This product might be a good option.")
  else:
    print("The average review score for this product is: " + str(average) + ". This product is a good option, it's recommended to buy. ")
    

link = input("Enter an amazon link: ")
Sure = input("Are you sure to analyze this link: ")
scrape(link, Sure)
df = pd.DataFrame()
df['Reviews']=review_content
df.to_csv('reviews.csv', index=True)
store()
openF()
result(average)


check = 0
while check != -1:
  answer = input("Do you want to try another product? ")
  if answer == "yes":
    link = input("Enter an amazon link: ")
    Sure = input("Are you sure to analyze this link: ")
    scrape(link, Sure)
    df = pd.DataFrame()
    df['Reviews']=review_content
    df.to_csv('reviews.csv', index=True)
    store()
    result(average)
  else:
    check = -1
    print("Thanks for using!")