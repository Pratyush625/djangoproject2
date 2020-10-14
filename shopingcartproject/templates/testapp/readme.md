To run locally, do the usual:

#. Create a Python 3.6 virtualenv Django 1.11 version installed

#. Create project projectname 
   
    django-admin startproject shopingcartproject

#. Go to the project dir 
   
    cd shopingcartproject

#. Create application inside main project directory 

    py manage.py startapp testapp

#. Configure the templatefile and staticfile(if required) inside settings.py 

#.Create template folder and static folder, inside static folder create css folder and image folder, insert the required images, here 3 html file has been used. base.html,additem.html,displayitem.html
Here Mysql used as  database

#. Configure Mysql in settings.py file
   
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sessiondb2',
        'USER': 'root',
        'PASSWORD':'root',
    }
}
#. Create database in Mysql DB
    

    create database sessiondb2;

#. Here template inheritance method is used

#. Create forms.py file inside testapp to enter the data

     from django import forms
     class AddItemForm(forms.Form):
        name=forms.CharField()
        quantity=forms.IntegerField()

#. Inside base.html
    

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    </head>

   <body>
    <div class="container" align='center'>
    {%block body_block%}
      
    {%endblock%}
   </div>
   </body>
    </html>

#. Inside additem.htnl
   

    <!DOCTYPE html>
   {% extends 'testapp/base.html'%}

      {%block body_block%}
      <h1>Add Item Form</h1>
       <form method="post">
           {{form.as_p}}
           {%csrf_token%}
           <input type="submit" class="btn btn-primary btn-large" value="Add Item">
       </form>
       <br><br>
       <a class="btn btn-primary" href="/display" role="button">Display Items</a>
       {%endblock%}

#. Inside display.html

     <!DOCTYPE html>
     {% extends 'testapp/base.html'%}

     {%block body_block%}
     <h1>Your Items information</h1>
     {% if request.session%}
     <table>
         <thead>
             <th>Name Of Item</th>
             <th>Quantity</th>
         </thead>
         {% for key,value in request.session.items%}
         <tr>
             <td>{{key}]</td>
             <td>{{value}]</td>
         </tr>
         {%endfor%}
        </table>
         {%else%}
         <p>No Items in Shopping cart</p>
         {%endif%}
     
       {%endblock%}


#. Define view function inside views.py 
   
    from django.shortcuts import render
    from testapp.forms import AddItemForm

     def add_item_view(request):
        form=AddItemForm()
      if request.method=='POST':
        name=request.POST['name']
        quantity=request.POST['quantity']
        request.session[name]=quantity
    return render(request,'testapp/additem.html',{'form':form})

    def display_item_view(request):
      return render(request,'testapp/displayitems.html')


#. To create session table inside Mysql database 

    py manage.py migrate

#. we can check the table in Mysql DB
   
    describe django_session;
    +--------------+-------------+------+-----+---------+-------+
    | Field        | Type        | Null | Key | Default | Extra |
    +--------------+-------------+------+-----+---------+-------+
    | session_key  | varchar(40) | NO   | PRI | NULL    |       |
    | session_data | longtext    | NO   |     | NULL    |       |
    | expire_date  | datetime(6) | NO   | MUL | NULL    |       |
    +--------------+-------------+------+-----+---------+-------+

#. After inserting data in the form we can check in mysql db(( Browser used- google chrome))

     mysql> select * from django_session;
  
         sessionkey                     |                     session_data                             | expiry date
   
     hqjhhs2y2xggds1df3f77wi66zzv88h2       NWU5YTk5NDA3MmFkYmI0YTU1MWM0ZThkZDQxMWI4ZmYwMjQwNmM5MT         2020-10-28 12:44:54.595692

     A session key, session data in encrypted form and session expiry data of inserted data has been created in DB(default 14 days)

#. If you insert the data again in db, the session key will be same but session_data and expiry date will be changed

#. If you add the the data from other browser like Internet Explorer then total 2 session key, 2 session data and 2 session expiry date      will  be created

          sessionkey                   |               session_data                                   |
                                                                                          
     8kqrr25rphc8y7hm9kmfgtywzwpps6xx       MWJjNDU3YzBjN2E0ZjgwMThhYzA1OWRiN2UzODE5Y2U1MWRhZDkyOT         2020-10-28 13:21:47.595723
     hqjhhs2y2xggds1df3f77wi66zzv88h2       NWU5YTk5NDA3MmFkYmI0YTU1MWM0ZThkZDQxMWI4ZmYwMjQwNmM5MT         2020-10-28 12:44:54.595692

#. We can set the session expiry time by using this command
   If we don't perform any operation on that time limit the session has automatically expired

     request.session.set_expiry(120) (120 is in seconds)

#. If we set 0 as argument, then session will expire once we close the browser

#. How to check expiry age and expiry date of session, but it gives the default age which is 14 days
     

     def session_info_view(request):
        session=request.session
        age=session.get_expiry_age()
        date=session.get_expiry_date()
        print('Expiry age',age)
        print('expiry date',date)

#. How to delete session data

    del request.session[sessionkey]

#. To delete all sessions
     
     for key in request.session.keys():
         del request.session[key]

    SESSION_SAVE_EVERY_REQUEST=True



#. Define view function inside urls.py

    from django.conf.urls import url
    from django.contrib import admin
    from testapp import views
   urlpatterns = [
       url(r'^admin/', admin.site.urls),
       url(r'^$', views.add_item_view),
       url(r'^display/', views.display_item_view),
       url(r'^info/', views.session_info_view),
    
     ]

#. To run server 

    py manage.py runserver
