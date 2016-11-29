import os
import unittest
from app import db, models
import hashlib
import datetime


# Function used to retrieve a user by its username
def retrieveUser(username):
    return db.session.query(models.Users).filter_by(username = username).first()


# Function used to retrieve all the existing posts
def retrievePosts():
    return models.Posts.query.all()


# Function used to retrieve all the existing comments
def retrieveComment():
    return models.Comments.query.all()



class TestCase(unittest.TestCase):
    def setUp(self):

        # Encrypt the passwords
        password1 = "testPassword"
        password2 = "secret-123"
        tmpPassword1 = hashlib.sha1()
        tmpPassword1.update(password1.encode('utf-8'))
        tmpPassword2 = hashlib.sha1()
        tmpPassword2.update(password2.encode('utf-8'))


        # Create 2 users
        user1 = models.Users(username = "paulMark",
                    password = tmpPassword1.hexdigest(), 
                    registration_date = datetime.datetime.utcnow(),
                    name = "Paul", surname = "Mark",
                    birth = "08/11/1997")

        user2 = models.Users(username = "marieBlum",
                    password = tmpPassword2.hexdigest(), 
                    registration_date = datetime.datetime.utcnow(),
                    name = "Marie", surname = "Blum",
                    birth = "14/05/1997")


        # Create 3 posts
        post1 = models.Posts(date = datetime.datetime.utcnow(), text = "Hi everyone!", author = user1, location = "Leeds UK",  
                    hates_number = 0,  comments_number = 0,  reports_number = 0)
        post2 = models.Posts(date = datetime.datetime.utcnow(), text = "This is my first post!", author = user2, location = "Paris FR",  
                    hates_number = 0,  comments_number = 0,  reports_number = 0)
        post3 = models.Posts(date = datetime.datetime.utcnow(), text = "And this one is my second one", author = user2, location = "London UK",  
                    hates_number = 0,  comments_number = 0,  reports_number = 0)


        # Create 4 dislikes
        hate1 = models.Hates(author = user1, post = post1)
        post1.hates_number += 1
        hate2 = models.Hates(author = user1, post = post2)
        post2.hates_number += 1
        hate3 = models.Hates(author = user2, post = post1)
        post1.hates_number += 1
        hate4 = models.Hates(author = user2, post = post2)
        post2.hates_number += 1


        # Create 3 comments
        comment1 = models.Comments(date = datetime.datetime.utcnow(), text = "Hello!", author = user1, post = post2)

        post2.comments_number += 1

        comment2 = models.Comments(date = datetime.datetime.utcnow(), text = "Yes!", author = user1, post = post3)

        post3.comments_number += 1

        comment3 = models.Comments(date = datetime.datetime.utcnow(), text = "I'm here!", author = user2, post = post1)

        post1.comments_number += 1


        # Create 2 reports
        report1 = models.Reports(author=user1, post=post2)
        post2.reports_number += 1
        report2 = models.Reports(author=user1, post=post3)
        post3.reports_number += 1


        # Add everything
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(hate1)
        db.session.add(hate2)
        db.session.add(hate3)
        db.session.add(hate4)
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.add(comment3)
        db.session.add(report1)
        db.session.add(report2)



    def tearDown(self):

        # Remove the changes
        db.session.remove()



    def test_users(self):

        # Retrieve the users
        user1 = retrieveUser("paulMark")
        user2 = retrieveUser("marieBlum")
        notExistingUser = retrieveUser("jelly")

        # Test if the users exist or not
        assert user1 != None
        assert user2 != None
        assert notExistingUser == None

        # Test the users information
        assert user1.username == "paulMark"
        assert user1.name == "Paul"
        assert user1.surname == "Mark"
        assert user1.birth == "08/11/1997"

        assert user2.username == "marieBlum"
        assert user2.name == "Marie"
        assert user2.surname == "Blum"
        assert user2.birth == "14/05/1997"


        # Encrypt the passwords
        password1 = "testPassword"
        password2 = "secret-123"
        tmpPassword1 = hashlib.sha1()
        tmpPassword1.update(password1.encode('utf-8'))
        tmpPassword2 = hashlib.sha1()
        tmpPassword2.update(password2.encode('utf-8'))

        # Test the passwords
        assert user1.password == tmpPassword1.hexdigest()
        assert user2.password == tmpPassword2.hexdigest()



    def test_posts(self):

        # Retrieve the posts
        post1 = retrievePosts()[-3]
        post2 = retrievePosts()[-2]
        post3 = retrievePosts()[-1]

        # Retrieve the users
        user1 = retrieveUser("paulMark")
        user2 = retrieveUser("marieBlum")


        # Test the posts informations
        assert post1.author == user1
        assert post1.location == "Leeds UK"
        assert post1.text == "Hi everyone!"

        assert post2.author == user2
        assert post2.location == "Paris FR"
        assert post2.text == "This is my first post!"

        assert post3.author == user2
        assert post3.location == "London UK"
        assert post3.text == "And this one is my second one"



    def test_hates(self):

        # Retrieve the posts
        post1 = retrievePosts()[-3]
        post2 = retrievePosts()[-2]
        post3 = retrievePosts()[-1]


        # Test the number of hates
        assert post1.hates_number == 2
        assert post2.hates_number == 2
        assert post3.hates_number == 0



    def test_comments(self):
        
        # Retrieve the users
        user1 = retrieveUser("paulMark")
        user2 = retrieveUser("marieBlum")

        # Retrieve the posts
        post1 = retrievePosts()[-3]
        post2 = retrievePosts()[-2]
        post3 = retrievePosts()[-1]

        # Retrieve the comments
        comment1 = retrieveComment()[-3]
        comment2 = retrieveComment()[-2]
        comment3 = retrieveComment()[-1]


        # Test if the comments have been created
        assert comment1 != None
        assert comment2 != None
        assert comment3 != None


        # Test the comments information
        assert comment1.author == user1
        assert comment1.text == "Hello!"
        assert comment1.post == post2

        assert comment2.author == user1
        assert comment2.text == "Yes!"
        assert comment2.post == post3

        assert comment3.author == user2
        assert comment3.text == "I'm here!"
        assert comment3.post == post1

    def test_reports(self):

        # Retrieve the posts
        post1 = retrievePosts()[-3]
        post2 = retrievePosts()[-2]
        post3 = retrievePosts()[-1]


        # Test the number of hates
        assert post1.reports_number == 0
        assert post2.reports_number == 1
        assert post3.reports_number == 1


if __name__ == '__main__':
    unittest.main()