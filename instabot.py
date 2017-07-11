from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='dc676a84b0334de7a435c57332f40b80')

model = app.models.get('food-items v1.0')

response = model.product_by_url('https://www.w3schools.com/css/trolltunga.jpg')

print response

import requests, urllib
from termcolor import colored
from accesstoken import APP_ACCESS_TOKEN
from user_detail import User, user_list,Recent_Media, media_list
from clarifai import rest
from clarifai.rest import ClarifaiApp
import json
import csv
BASE_URL = 'https://api.instagram.com/v1/'


# Function retrieve owner's information


def self_info():
    print "Displaying Own Information"
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    try:
        owner_info = requests.get(request_url).json()
        if owner_info['meta']['code'] == 200:  # HTTP 200 means transmission is OK
            if len(owner_info['data']):
                print colored("Username: ", "red"), '%s' % colored(owner_info['data']['username'], "blue")
                print colored('Number of followers: ', "red"), '%s' % colored(owner_info['data']['counts']['followed_by'], "blue")
                print colored('Number of people you are following: ', "red"), '%s' % colored(owner_info['data']['counts']['follows'],
                                                                                             "blue")
                print colored('Number of posts: ', "red"), '%s' % colored(owner_info['data']['counts']['media'], "blue")
                print owner_info
            else:
                print 'User does not exist!'
        else:
            print 'Status code other than 200 received!'
    except:
        print "Something Wrong with the url"

# Function to add user using username and generate corresponding user id


def add_user():
    username = raw_input("Enter Username: ")
    try:
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (username, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                id = user_info['data'][0]['id']
                # print id
                # print user_info
                print "User has been added successfully!!"
                user_list.append(User(username, id))
            else:
                print "Invalid username!!"
        else:
            print "Status code not 200!"
    except:
        print "Url request exception occurred!"

# Function to select user for further operations


def select_user():
    if not user_list:
        return None
    else:
        index = 1
        for i in range(0, len(user_list)):
            print '%d.  %s' % (index, user_list[i].name)
            index = index + 1
        while True:
            choice = raw_input("Enter Your Choice: ")
            try:
                choice = int(choice)
                break
            except:
                print colored("Enter Valid Choice", "red")
        choice = int(choice)
        return choice - 1

# Function to fetch user details by selecting a user


def fetch_user_details():
    index = select_user()
    if index is not None:
        id1 = user_list[index].id
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (id1, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        try:
            user_info = requests.get(request_url).json()
            if user_info['meta']['code'] == 200:  # HTTP 200 means transmission is OK
                if len(user_info['data']):
                    print colored("Username: ", "red"), '%s' % colored(user_info['data']['username'], "blue")
                    if len(user_info['data']['bio']):
                        print colored("Bio: ", "red"), '%s' % colored(user_info['data']['bio'], "blue")
                    else:
                        print colored("Bio: ", "red"), '%s' % colored("No Bio in his profile", "blue")
                    print colored('Number of followers: ', "red"), '%s' % colored(user_info['data']['counts']['followed_by'], "blue")
                    print colored('Number of people you are following: ', "red"), '%s' % colored(
                        user_info['data']['counts']['follows'],
                        "blue")
                    print colored('Number of posts: ', "red"), '%s' % colored(user_info['data']['counts']['media'], "blue")
                    # print user_info
                else:
                    print 'User does not exist!'
            else:
                print 'Status code other than 200 received!'
        except:
            print "Something Wrong with the url"
    else:
        print 'Add Users Please'


# Function to fetch  self recent posts.


def fetch_own_recent_posts():
    count = int(raw_input("Enter number of posts you want to retrieve: "))
    try:
        request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s&count=%d') % (ACCESS_TOKEN, count)
        print 'GET request url : %s' % (request_url)
        own_media = requests.get(request_url).json()
        if own_media['meta']['code'] == 200:
            if len(own_media['data']):
                if len(own_media['data']) >= count:
                    for i in range(0, count):
                        image_name = own_media['data'][i]['id'] + '.jpeg'
                        image_url = own_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print 'Your image has been downloaded!'
                else:
                    print "Your count limit exceeds bye user total posts"
                print own_media
            else:
                print 'Post does not exist!'
        else:
            print 'Status code other than 200 received!'
    except:
        print "Something wrong with url"

# Function to fetch  recent posts of  user by selecting it from list.


def fetch_user_recent_posts():
    index = select_user()
    if index is not None:
        id1 = user_list[index].id
        name = user_list[index].name
        if not media_list:
            count = int(raw_input("Enter number of posts you want to retrieve: "))
            try:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s&count=%d') % (id1, ACCESS_TOKEN, count)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()
                if user_media['meta']['code'] == 200:
                    if len(user_media['data']):
                        if len(user_media['data']) >= count:
                            for i in range(0, count):
                                media_id = user_media['data'][i]['id']
                                media_type = user_media['data'][i]['type']
                                media_url = user_media['data'][i]['images']['standard_resolution']['url']
                                media_likes = user_media['data'][i]['likes']['count']
                                media_list.append(Recent_Media(name, media_id, media_type, media_url, media_likes))
                                ch = raw_input("Do you want to download image (y/n): ")
                                if ch.upper() == 'Y':
                                    image_name = user_media['data'][i]['id'] + '.jpeg'
                                    urllib.urlretrieve(media_url, image_name)
                                    print 'Your image has been downloaded!'
                        else:
                            print "Your count limit exceeds bye user total posts"
                    else:
                        print 'Post does not exist!'
                else:
                    print 'Status code other than 200 received!'
            except:
                print "Something wrong with url"
    else:
        print "Please Add Users"


def like_recent_post():
    index = select_user()
    name = user_list[index].name
    if index is not None:
        for i in range(0, len(media_list)):
            if media_list[i].name == name:
                media_id = media_list[i].media_id
                try:
                    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
                    print 'GET request url : %s' % (request_url)
                    payload = {'access_token': ACCESS_TOKEN}
                    post_like = requests.post(request_url, payload).json()
                    if post_like['meta']['code'] == 200:
                        print "You have liked the pic successfully!!"
                        break
                    else:
                        print "Status code not 200!"
                        break
                except:
                    print "Url request exception occurred!!!"
                    break
    else:
        print "Please add users!!"


def delete_like():
    index = select_user()
    name = user_list[index].name
    if index is not None:
        for i in range(0, len(media_list)):
            if media_list[i].name == name:
                media_id = media_list[i].media_id
                try:
                    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
                    print 'GET request url : %s' % (request_url)
                    delete_like = requests.delete(request_url).json()
                    if delete_like['meta']['code'] == 200:
                        print "You have unliked the pic successfully!!"
                        break
                    else:
                        print "Status code not 200!"
                        break
                except:
                    print "Url request exception occurred!!!"
                    break
    else:
        print "Please add users!!"


def post_comment():
    index = select_user()
    name = user_list[index].name
    if index is not None:
        for i in range(0, len(media_list)):
            if media_list[i].name == name:
                media_id = media_list[i].media_id
                try:
                    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
                    print 'GET request url : %s' % (request_url)
                    list_comment = requests.get(request_url).json()
                    if list_comment['meta']['code'] == 200:
                        print "Your comment has been successfully posted!!!!"
                        break
                    else:
                        print "Status code not 200!"
                        break
                except:
                    print "Url request exception occurred!!!"
                    break
    else:
        print "Please add users!!"


def list_comment():
    index = select_user()
    name = user_list[index].name
    if index is not None:
        for i in range(0, len(media_list)):
            if media_list[i].name == name:
                media_id = media_list[i].media_id
                try:
                    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
                    print 'GET request url : %s' % (request_url)
                    post_like = requests.get(request_url).json()
                    if post_like['meta']['code'] == 200:
                        for i in range(0, len(post_like['data'])):
                            print "%s  commented by: %s" % (post_like['data'][i]['text'], post_like['data'][i]['from']['username'])
                        break
                    else:
                        print "Status code not 200!"
                        break
                except:
                    print "Url request exception occurred!!!"
                    break
    else:
        print "Please add users!!"


def get_images():
    app = ClarifaiApp(api_key='c421a2e2717246b09706b18c36039e79')
    model = app.models.get("general-v1.3")
    app.inputs.delete_all()
    # data1 = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
    # print data1
    # with open('abc.json', 'wb') as outfile:
    #     json.dump(data1, outfile)
    # print data1['outputs'][0]['data']['concepts'][0]['name']
    # mriutestbot id
    id = 5716892371
    media = {}
    image_list = []
    url_list = []
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for i in range(0, len(user_media['data'])):
                media = {}
                print user_media['data'][i]['images']['low_resolution']['url']
                media['media_url'] = user_media['data'][i]['images']['low_resolution']['url']
                media['latitude'] = user_media['data'][i]['location']['latitude']
                media['longitude'] = user_media['data'][i]['location']['longitude']
                app.inputs.create_image_from_url(media['media_url'])
                image_list.append(media)
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    data1 = app.inputs.search_by_predicted_concepts(concept='cyclone')
    data2 = app.inputs.search_by_predicted_concepts(concept='flood')
    data3 = app.inputs.search_by_predicted_concepts(concept='drought')
    data4 = app.inputs.search_by_predicted_concepts(concept='earthquake')
    print len(data1)
    for i in range(0, len(data1)):
        print data1[i].url
        url = {}
        url['url'] = data1[i].url
        url['name'] = 'Cyclone'
        url_list.append(url)

    for i in range(0, len(data2)):
        url = {}
        print data2[i].url
        url['url'] = data2[i].url
        url['name'] = 'flood'
        url_list.append(url)

    for i in range(0 , len(data3)):
        url = {}
        print data3[i].url
        url['url'] = data3[i].url
        url['name'] = 'drought'
        url_list.append(url)

    for i in range(0 ,len(data4)):
        url = {}
        print data4[i].url
        url['url'] = data4[i].url
        url['name'] = 'earthquake'
        url_list.append(url)
    print url_list
    print image_list
    with open('image.csv', 'a') as out:
        writer = csv.DictWriter(out, fieldnames=['Url', 'Longitude', 'Latitude', 'Name'], delimiter=',')
        writer.writeheader()
        for i in range(0, len(url_list)):
            for j in range(0 ,len(image_list)):
                if url_list[i]['url'] == image_list[j]['media_url']:
                    print 'hello'
                    writer.writerow({'Url': image_list[j]['media_url'], 'Latitude': image_list[j]['latitude'],
                                     'Longitude': image_list[j]['longitude'], 'Name': url_list[i]['name']})


def start():

    while True:
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "1.Get your own details"
        print "2.Add User"
        print "3.Fetch User Details"
        print "4.Fetch your own recent post"
        print "5.Fetch the recent post of a user"
        print "6.Like the most recent post of a user"
        print "7.Unlike the most recent post of a user"
        print "8.Post a comment on user's recent post"
        print "9.Get a list of comments on user's recent post"
        print "10.Getting natural Calamities Images"
        print "11.Exit"
        while True:
            choice = raw_input("Enter Your Choice: ")
            try:
                choice = int(choice)
                break
            except:
                print 'Please Enter Valid Option'
        choice = int(choice)
        if choice == 1:
            self_info()
        elif choice == 2:
            add_user()
        elif choice == 3:
            fetch_user_details()
        elif choice == 4:
            fetch_own_recent_posts()
        elif choice == 5:
            fetch_user_recent_posts()
        elif choice == 6:
            like_recent_post()
        elif choice == 7:
            delete_like()
        elif choice == 8:
            post_comment()
        elif choice == 9:
           list_comment()
        elif choice == 10:
           get_images()
        elif choice == 11:
            exit()
        else:
            print "Enter valid option"
        ch = raw_input("Do you wish to continue: y/n  ")
        if ch.upper() == "N":
            break
start()